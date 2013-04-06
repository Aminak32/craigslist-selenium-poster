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
#from postGetter import getPage

TIMEOUT_ = 20 #20 second timeout to wait

class ServiceAutomator():
	def __init__(self, baseUrl, commandStr, driver="firefox", verbose=False, dont_close=False, proxy=None):
		self.verbose = verbose
		self.dont_close = dont_close
		self.address = "/bbb"								#address of services page
		if self.verbose:
			print "Initializing %s automator" %(ServiceAutomator.__name__)
			print "Base url:",baseUrl
			print "Will be using", driver, "as webdriver"
	
		try:
			if proxy: self.setProxy(proxy)
			elif driver == "chrome":
				self.driver = webdriver.Chrome()
			else:
				self.driver = webdriver.Firefox()
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

		#selecting which service category to continue
		base_xpath = """//*[@id="pagecontainer"]/section/form/blockquote/label[%d]/input"""
		if self.category == 'service_automotive': xpath = base_xpath %(1)
		elif self.category == 'service_beauty': xpath = base_xpath %(2)
		elif self.category == 'service_computer': xpath = base_xpath %(3)
		elif self.category == 'service_creative': xpath = base_xpath %(4)
		elif self.category == 'service_cycle': xpath = base_xpath %(5)
		elif self.category == 'service_event': xpath = base_xpath %(6)
		elif self.category == 'service_farm': xpath = base_xpath %(7)
		elif self.category == 'service_financial': xpath = base_xpath %(8)
		elif self.category == 'service_household': xpath = base_xpath %(9)
		elif self.category == 'service_labor': xpath = base_xpath %(10)
		elif self.category == 'service_legal': xpath = base_xpath %(11)
		elif self.category == 'service_lessons': xpath = base_xpath %(12)
		elif self.category == 'service_marine': xpath = base_xpath %(13)
		elif self.category == 'service_pet': xpath = base_xpath %(14)
		elif self.category == 'service_real_estate': xpath = base_xpath %(15)
		elif self.category == 'service_skill': xpath = base_xpath %(16)
		elif self.category == 'service_small_biz_ads': xpath = base_xpath %(17)
		elif self.category == 'service_therapeutic': xpath = base_xpath %(18)
		elif self.category == 'service_travel': xpath = base_xpath %(19)
		elif self.category == 'service_write': xpath = base_xpath %(20)

		if self.verbose: print "Category Selected:", self.category
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
			if self.verbose: print "Waiting for a few seconds..."
			sleep(10)
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

	def setProxy(self, myproxy):
		if self.verbose: print "Attempting to set proxy to", myproxy
		
		proxy = Proxy({
		    'proxyType': ProxyType.MANUAL,
		    'httpProxy': myproxy,
		    'ftpProxy': myproxy,
		    'sslProxy': myproxy,
		    'noProxy': '' # set this value as desired
		    })

		self.driver = webdriver.Firefox(proxy=proxy)
		if self.verbose: print "Firefox proxy is set to",myproxy

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
		if self.verbose: print "Prompting server to verify email...."
		time_to_wait = ranndom.randint(120-200)
		if self.verbose: print "Will wait for", time_to_wait, "seconds"
		sleep(time_to_wait)
		if self.verbose: print "Connecting to server"
		url = "http://%s/ws.php?action=get_post_confirm_url_via_email&schedule_id=%s"%(self.commands['poster_address'], self.commands['schedule_id'])
		response = getPage(url)
		if self.verbose: print "Response:", response


