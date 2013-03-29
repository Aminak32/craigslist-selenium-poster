#!/usr/bin/env python

""" Craigslist poster application using selenium API
	Service poster sub-script
	@author Ivan Dominic Baguio - baguio.ivan@gmail.com """

from BaseAutomator import *

class ServicesAutomator(BaseAutomator):
	def __init__(self, baseUrl, commandStr, category, driver="firefox", verbose=False, dont_close=False):
		self.automator_name = ServicesAutomator.__name__
		self.address = "/bbb"								#address of services page
		BaseAutomator.__init__(self,baseUrl,commandStr,driver,verbose,dont_close)
		self.category = category

		#some xpaths
		self.upload_xpath = """//*[@id="pagecontainer"]/section/div/div[1]/div/form/input[3]""" #upload xpath of Services
		self.done_xpath = """//*[@id="pagecontainer"]/section/form/button"""
		self.publish_xpath = """//*[@id="pagecontainer"]/section/div[1]/form/button"""

	def loadCommands(self, commandStr):
		self.commands = json.loads(commandStr)
		if not 'privacy' in self.commands: self.commands['privacy'] = 'anonymize'
		if not 'images' in self.commands: self.commands['images'] = []

	def automate(self):
		BaseAutomator.automate(self)			#do the basic loading of page and driver window
		driver = self.driver

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
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		btn.click()

		sleep(1)
		labels = len(driver.find_elements_by_tag_name("label"))
		if self.verbose: print "Randomizing nearest city. Randoming from 1-",labels
		xpath = """//*[@id="pagecontainer"]/section/form/blockquote/label[%d]/input""" % random.randint(1,labels)
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		btn.click()

		if self.verbose: print "Waiting for form to load..."
		xpath = """//*[@id="postingForm"]/button"""
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))

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
		inpt.send_keys(self.commands['sloc'])

		inpt = driver.find_element_by_xpath(email_xpath)
		inpt.send_keys(self.commands['email'])

		inpt = driver.find_element_by_xpath(email2_xpath)
		inpt.send_keys(self.commands['email'])

		inpt = driver.find_element_by_xpath(post_xpath)
		inpt.send_keys(self.commands['post'])

		btn = driver.find_element_by_xpath(privacy_xpath[self.commands['privacy']])
		btn.click()

		if self.commands['ok_contact'] == "yes":
			okcontact_xpath = """//*[@id="oc"]"""
			btn = driver.find_element_by_xpath(okcontact_xpath)
			btn.click()

		if self.verbose: print "Continue..."
		form_xpath = """//*[@id="postingForm"]"""
		btn = driver.find_element_by_xpath(form_xpath)
		btn.submit()

		self.uploadImages()
		BaseAutomator.finish(self)

"""DOCUMENTATION for Services
	See documentation for BaseAutomator for an Overview.

	Categories handled by this class:
	<category> 			service_automotive
						service_beauty
						service_biz_ads
						service_computer
						service_creative
						service_cycle
						service_event
						service_farm
						service_financial
						service_household
						service_labor
						service_legal
						service_lessons
						service_marine
						service_pet
						service_real_estate
						service_skill
						service_therapeutic
						service_travel
						service_write

	REQUIRED COMMANDS FOR Services (aside from Base Commands in BaseAutomator):
		None

	OPTIONAL COMMANDS:
		KEY 		DESCRIPTION
		privacy 	choices = 'show', 'hide', 'anonymize'. Default is 'anonymize'

	EXAMPLE:
	For example, you would like to post a labor & moving listing on Craigslist miami.
	Setup first the commands/info needed for the post, sample below:

		info = {"title": "Labor for carpentry",
				"sloc": "970 NE 78th St, Miami FL",
				"email": "myemail@gmail.com",
				"post": "I need someone to do some carpentry jobs in my house. Blah blah blah",
				"ok_contact":"yes",
				"privacy": "show",
				"images": ['/home/Documents/images/carpentry1.jpg','/home/Documents/images/carpentry2.jpg']}

		ENCODE the above info as a VALID JSON. then run the code below on the command line:
		python clposter.py miami service_labor <encoded_json_string>
"""