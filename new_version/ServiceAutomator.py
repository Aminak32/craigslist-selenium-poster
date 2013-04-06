#!/usr/bin/
import sys, json, random
from myhttplib import getPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.proxy import *
from time import sleep

TIMEOUT_ = 20 #20 second timeout to wait

class ServiceAutomator():
	def __init__(self, baseUrl, commandStr, browser="firefox", verbose=False, dont_close=False, proxy=None):
		self.verbose = verbose
		self.dont_close = dont_close
		self.address = "/bbb"								#address of services page
		if self.verbose:
			print "Initializing %s automator" %(ServiceAutomator.__name__)
			print "Base url:",baseUrl
			print "Will be using",browser,"as browser"
	
		try:
			if proxy: self.setProxy(proxy,browser)
			elif browser == "chrome":
				self.driver = webdriver.Chrome()
			elif browser == "firefox":
				self.driver = webdriver.Firefox()
			else:
				print "Invalid driver",browser,"will quit"
				sys.exit(0)
		except Exception, e:
			print e
			sys.exit(0)

		self.loadCommands(commandStr)						#loads the commands from JSON, see docu below
		self.baseUrl = baseUrl
		self.logged_in = False

		self.upload_xpath = """//*[@id="pagecontainer"]/section/div/div[1]/div/form/input[3]""" #upload xpath of Services
		self.done_xpath = """//*[@id="pagecontainer"]/section/form/button"""
		self.publish_xpath = """//*[@id="pagecontainer"]/section/div[1]/form/button"""

	def automate(self):
		driver = self.driver
		if self.commands['username'] and self.commands['password']:
			self.login(self.commands['username'],self.commands['password'])

		#go to base url
		if self.verbose: print "Loading %s page..." %(ServiceAutomator.__name__)
		driver.get("https://"+self.baseUrl+self.address)

		if self.verbose: print "Clicking post url"
		xpath="""//*[@id="ef"]/a[2]"""						#the xpath of the post btn/link.
		btn = driver.find_element_by_xpath(xpath)
		btn.click()

		#xpath for service_labor
		xpath = """//*[@id="pagecontainer"]/section/form/blockquote/label[10]/input"""

		try:
			btn = WebDriverWait(driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)
		btn.click()

		sleep(1)
		base_xpath = """//*[@id="pagecontainer"]/section/form/blockquote/label[%d]/input""" 
		if not self.commands['county']:
			labels = len(driver.find_elements_by_tag_name("label"))
			if self.verbose: print "Randomizing nearest city. Randoming from 1-",labels
			xpath = base_xpath % random.randint(1,labels)
		else:
			xpath = base_xpath % int(self.commands['county'])
		try:
			btn = WebDriverWait(driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)
		
		btn.click()

		if self.verbose: print "Waiting for form to load..."
		xpath = """//*[@id="postingForm"]/button"""

		try:
			btn = WebDriverWait(driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)

		#Write stuff to text inputs
		if self.verbose: print "Loading xpaths of text inputs"
		title_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[1]/input"""
		sloc_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[3]/input"""
		email_xpath = """//*[@id="FromEMail"]"""
		email2_xpath = """//*[@id="ConfirmEMail"]"""

		post_xpath = """//*[@id="postingForm"]/div/div[1]/textarea"""
		privacy_xpath = {'show': """//*[@id="P"]""", 'hide': """//*[@id="A"]""", 'anonymize': """//*[@id="oiab"]/label[3]/input"""}

		if self.verbose: print "Writing values to text inputs"

		inpt = driver.find_element_by_xpath(title_xpath)
		inpt.send_keys(self.commands['title'])

		inpt = driver.find_element_by_xpath(sloc_xpath)
		inpt.send_keys(self.commands['location'])

		if not self.logged_in:
			inpt = driver.find_element_by_xpath(email_xpath)
			inpt.send_keys(self.commands['email'])

			inpt = driver.find_element_by_xpath(email2_xpath)
			inpt.send_keys(self.commands['email'])

		inpt = driver.find_element_by_xpath(post_xpath)
		inpt.send_keys(self.commands['body'])

		btn = driver.find_element_by_xpath(privacy_xpath[self.commands['privacy']])
		btn.click()

		if self.commands['zip']:
			#code not yet finished
			if self.verbose: print "Adding info on maps"
			map_xpath = """//*[@id="wantamap"]"""
			btn = driver.find_element_by_xpath(map_xpath)
			btn.click()
			#xpaths for the other fields in map. ignore for now
			"""//*[@id="xstreet0"]"""
			"""//*[@id="xstreet1"]"""
			"""//*[@id="city"]"""
			"""//*[@id="region"]"""
			zip_xpath = """//*[@id="postal_code"]"""
			btn = driver.find_element_by_xpath(zip_xpath)
			btn.send_keys(self.commands['zip'])
			
		if self.commands['ok_contact'] == "yes":
			okcontact_xpath = """//*[@id="oc"]"""
			btn = driver.find_element_by_xpath(okcontact_xpath)
			btn.click()

		if self.verbose: print "Continue..."
		form_xpath = """//*[@id="postingForm"]"""
		btn = driver.find_element_by_xpath(form_xpath)
		btn.submit()

		if self.commands['zip']:
			if self.verbose: print "Continuing from maps..."
			continue_xpath = """//*[@id="leafletForm"]/button[1]"""
			btn = driver.find_element_by_xpath(continue_xpath)
			btn.submit()

		self.uploadImages()
		self.finish()
		self.verifyEmail()

		if not self.dont_close:
			close_time = random.randint(1,3)
			print "Closing browser in ",close_time,"seconds..."
			sleep(close_time)
			self.driver.close()
		else:
			print "Will not close browser"

	def uploadImages(self):
		if self.verbose: print "Uploading images..."
		print self.commands['images']
		for img in self.commands['images']:
			if self.verbose: print "Uploading ",img
			try:
				inpt = WebDriverWait(self.driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, self.upload_xpath)))
			except Exception, e:
				print "Timeout Error. Page took to long to load. Try again later. Will terminate"
				sys.exit(0)
			inpt.send_keys(img)
			if self.verbose: print "Waiting for a few seconds till image uploads..."
			sleep(random.randint(50,120))
			inpt = WebDriverWait(self.driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, self.upload_xpath)))

	def loadCommands(self, commands):
		self.commands = commands#json.loads(commandStr)
		if not 'privacy' in self.commands: self.commands['privacy'] = 'anonymize'
		if not 'images' in self.commands: self.commands['images'] = []
		if not 'ok_contact' in self.commands: self.commands['ok_contact'] = True

	def finish(self):
		"""Do finishing stuffs"""
		if self.verbose: print "Finalizing post..."
		try:
			btn = WebDriverWait(self.driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, self.done_xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)
		btn.click()

		if self.verbose: print "Publishing post..."
		try:
			btn = WebDriverWait(self.driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, self.publish_xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)
		btn.click()

		if not self.dont_close:
			if self.verbose: print "Quiting browser..."
			self.driver.quit()

	def setProxy(self, myproxy,browser):
		if self.verbose: print "Attempting to set proxy to", myproxy
		
		if browser == "firefox":
			proxy = Proxy({
			    'proxyType': ProxyType.MANUAL,
			    'httpProxy': myproxy,
			    'ftpProxy': myproxy,
			    'sslProxy': myproxy,
			    'noProxy': '' # set this value as desired
			    })

			self.driver = webdriver.Firefox(proxy=proxy)
		elif driver == "chrome":
			webdriver.DesiredCapabilities.INTERNETEXPLORER['proxy'] = {
			    "httpProxy":myproxy,
			    "ftpProxy":myproxy,
			    "sslProxy":myproxy,
			    "noProxy":None,
			    "proxyType":"MANUAL",
			    "class":"org.openqa.selenium.Proxy",
			    "autodetect":False
			}
			self.driver = webdriver.Chrome()
		if self.verbose: print browser,"proxy is set to",myproxy

	def login(self, username, password):
		"""Goes to the main account page, and checks if the logged in account is the same as the
		account to be logged in. If not, logout the current account, and login the new one. If no
		account is logged in. Log ins the account"""

		if self.verbose: print "Attempting to log in..."
		self.driver.get("https://accounts.craigslist.org/login")

		try:
			#check if a user is already logged in
			if self.verbose: print "Checking if a user is already logged in.."
			username_xpath = """/html/body/div/a[2]"""
			btn = self.driver.find_element_by_xpath(username_xpath)
			if usrname in btn.text:
				if self.verbose: print "User already logged in..."
				return
			else:
				print "User logged in is not the user, will logout and login again..."
				logout_xpath = """//*[@id="ef"]/a[1]"""
				btn = self.driver.find_element_by_xpath(logout_xpath)
				btn.click()
		except Exception, e:
			if self.verbose: print "No User is logged in. Will continue to log in."

		#continue with login credentials
		if self.verbose: print "Logging in. USERNAME: %s PASSWORD: %s" %(username,password)
		username_xpath = """//*[@id="inputEmailHandle"]"""
		password_xpath = """//*[@id="inputPassword"]"""
		form_xpath = """//*[@id="pagecontainer"]/section/form"""
		try:
			btn = WebDriverWait(self.driver,TIMEOUT_).until(EC.presence_of_element_located((By.XPATH, username_xpath)))
		except Exception, e:
			print "Timeout Error. Page took to long to load. Try again later. Will terminate"
			sys.exit(0)

		btn.send_keys(username)
		btn = self.driver.find_element_by_xpath(password_xpath)
		btn.send_keys(password)

		form = self.driver.find_element_by_xpath(form_xpath)
		form.submit()
		self.logged_in = True
		if self.verbose: print "Logged in completed!"

	def verifyEmail(self):
		if self.verbose: print "Prompting server to verify email..."
		time_to_wait = random.randint(140,200)
		if self.verbose: print "Will wait for", time_to_wait, "seconds"
		sleep(time_to_wait)
		if self.verbose: print "Connecting to server..."
		url = "http://%s/ws.php?action=get_post_confirm_url_via_email&schedule_id=%s"%(self.commands['poster_address'], self.commands['schedule_id'])
		response = json.loads(getPage(url))
		if self.verbose: print "Response:", response
		if response['status'] == 'true':
			print "Server responded OK for verification!"