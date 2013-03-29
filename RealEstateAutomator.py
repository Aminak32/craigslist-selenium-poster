#!/usr/bin/env python

""" Craigslist poster application using selenium API
	Real Estate poster sub-script
	@author Ivan Dominic Baguio - baguio.ivan@gmail.com """

from BaseAutomator import *

class RealEstateAutomator(BaseAutomator):
	def __init__(self, baseUrl, commandStr, driver="firefox", verbose=False, dont_close=False):
		self.automator_name = RealEstateAutomator.__name__
		self.address = "/rea"								#address of real estate page
		BaseAutomator.__init__(self,baseUrl,commandStr,driver,verbose, dont_close)

		#some xpaths
		self.upload_xpath = """//*[@id="pagecontainer"]/section[2]/div/div[1]/div/form/input[3]"""
		self.done_xpath = """//*[@id="pagecontainer"]/section[2]/form/button"""
		self.publish_xpath = """//*[@id="pagecontainer"]/section[2]/div[1]/form/button"""

	def automate(self):
		BaseAutomator.automate(self)			#do the basic loading of page and driver window
		driver = self.driver
		#selecting real estate type
		if self.commands['re_type'] == 'offer':
			xpath = """//*[@id="pagecontainer"]/section[2]/form/label[1]/input"""	#xpath for the offer radio
			if self.verbose: print "RealEsate type:OFFER selected"
		elif self.commands['re_type'] == 'need':
			xpath = """//*[@id="pagecontainer"]/section[2]/form/label[2]/input"""	#xpath for the needed radio
			if self.verbose: print "RealEsate type:NEED selected"
		else:
			xpath = ""
			if self.verbose: print "RealEsate type:NONE selected"

		if self.verbose: print "Waiting for button to load..."
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		btn.click()

		#selecing category
		if self.commands['re_type'] == 'offer':
			base_xpath = """//*[@id="pagecontainer"]/section[2]/form/blockquote/label[%d]/input"""
			if self.commands['re_category'] == "rooms": xpath = base_xpath %(1)
			elif self.commands['re_category'] == "rent": xpath = base_xpath %(2)
			elif self.commands['re_category'] == "swap": xpath = base_xpath %(3)
			elif self.commands['re_category'] == "ofc": xpath = base_xpath %(4)
			elif self.commands['re_category'] == "park": xpath = base_xpath %(5)
			elif self.commands['re_category'] == "re_broker": xpath = base_xpath %(6)
			elif self.commands['re_category'] == "re_owner": xpath = base_xpath %(7)
			elif self.commands['re_category'] == "temp": xpath = base_xpath %(8)
			elif self.commands['re_category'] == "vacation": xpath = base_xpath %(9)

		elif self.commands['re_type'] == 'need':
			if self.commands['re_category'] == "apts": xpath = base_xpath %(1)
			elif self.commands['re_category'] == "re_wanted": xpath = base_xpath %(2)
			elif self.commands['re_category'] == "share": xpath = base_xpath %(3)
			elif self.commands['re_category'] == "temp": xpath = base_xpath %(4)
		else:
			xpath = ""
			if self.verbose: print "No category selected"

		if self.verbose: print "Category selected:", self.commands['re_category']
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		#btn = driver.find_element_by_xpath(xpath)
		btn.click()

		#randomize nearest location/city
		sleep(1)
		labels = len(driver.find_elements_by_tag_name("label"))
		if self.verbose: print "Randomizing nearest city. Randoming from 1-",labels
		xpath = """//*[@id="pagecontainer"]/section[2]/form/blockquote/label[%d]/input""" % random.randint(1,labels)
		#btn = driver.find_element_by_xpath(xpath)
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		btn.click()

		if self.verbose: print "Loading xpaths of text inputs"
		if int(self.commands['bedroom']) == -1:
			price_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[1]/input"""
			sqft_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[2]/input"""
			title_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[3]/input"""
			sloc_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[5]/input"""
		else:
			price_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[1]/input"""
			br_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[2]/select"""
			sqft_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[3]/input"""
			title_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[4]/input"""
			sloc_xpath = """//*[@id="postingForm"]/div/div[1]/div[1]/div[6]/input"""

		email_xpath = """//*[@id="FromEMail"]"""
		email2_xpath = """//*[@id="ConfirmEMail"]"""
		post_xpath = """//*[@id="postingForm"]/div/div[1]/textarea"""
		
		privacy_xpath = {'show': """//*[@id="P"]""", 'hide': """//*[@id="A"]""", 'anonymize': """//*[@id="oiab"]/label[3]/input"""}
		
		if self.verbose: print "Waiting for form to load..."
		xpath = """//*[@id="postingForm"]/button"""
		btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, xpath)))

		if self.verbose: print "Writing values to text inputs"
		inpt = driver.find_element_by_xpath(price_xpath)
		inpt.send_keys(self.commands['price'])

		if self.verbose: "bedroom: ", self.commands['bedroom']
		if int(self.commands['bedroom']) > 0:
			inpt = driver.find_element_by_xpath(br_xpath)
			inpt.send_keys(self.commands['bedroom'])

		inpt = driver.find_element_by_xpath(sqft_xpath)
		inpt.send_keys(self.commands['sqft'])

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

		if self.commands['show_maps']:
			#code not yet finished
			if self.verbose: print "Adding info on maps"
			map_xpath = """//*[@id="wantamap"]"""
			btn = driver.find_element_by_xpath(map_xpath)
			btn.click()

			"""//*[@id="xstreet0"]"""
			"""//*[@id="xstreet1"]"""
			"""//*[@id="city"]"""
			"""//*[@id="region"]"""
			"""//*[@id="postal_code"]"""

		if self.commands['ok_cats'] == "yes":
			if self.verbose: print "Cats are allowed"
			okcats_xpath = """//*[@id="perms"]/label[1]/input"""
			btn = driver.find_element_by_xpath(okcats_xpath)
			btn.click()

		if self.commands['ok_dogs'] == "yes":
			if self.verbose: print "Dogs are allowed"
			okdogs_xpath = """//*[@id="perms"]/label[2]/input"""
			btn = driver.find_element_by_xpath(okdogs_xpath)
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

	def loadCommands(self, commandStr):
		self.commands = json.loads(commandStr)
		if not 'subloc' in self.commands: self.commands['subloc'] = "";
		if not 'privacy' in self.commands: self.commands['privacy'] = 'anonymize'
		if not 'bedroom' in self.commands: self.commands['bedroom'] = -1;
		if not 'show_maps' in self.commands: self.commands['show_maps'] = False
		if not 'ok_cats' in self.commands: self.commands['ok_cats'] = False
		if not 'ok_dogs' in self.commands: self.commands['ok_dogs'] = False
		if not 'ok_contact' in self.commands: self.commands['ok_contact'] = False

"""DOCUMENTATION for RealEsate
	See documentation for BaseAutomator for an Overview.

		<category> 			housing_real_estate

	REQUIRED COMMANDS FOR RealEsate (aside from Base Commands in BaseAutomator):
		KEY 		DESCRIPTION
		price 		price of the listing
		sqft 		area of the real estate
		re_type 	real estate type. Choices 'offer' or 'need'
		re_category	the subcategory for the real estate
					these are the categories asked by Craigslist when posting real estate

			below are the possible value of re_category
				KEY 		DESCRIPTION 					bedroom Required?
			for offer:
				rooms		rooms & shares					No
				rent 		apts/housing for rent 			Yes
				swap 		housing swap 					Yes
				ofc 		office & commercial 			No
				park 		parking & storage 				No
				re_broker	real estate by broker 			Yes
				re_owner 	real estate by owner 			Yes
				temp 		sublets & temporary 			Yes
				vacation 	vacation rentals 				Yes
			for need:
				apts		apts wanted
				re_wanted 	real estate wanted
				share 		room/share wanted
				temp 		sublet/temp

	OPTIONAL COMMANDS:
		KEY 		DESCRIPTION
		privacy 	choices = 'show', 'hide', 'anonymize'. Default is 'anonymize'
		bedroom		number of bedrooms.
		show_maps	show maps, not yet finished
		ok_cats		check OK Cats (yes/no)
		ok_dogs		check OK Dogs (yes/no)

	EXAMPLE:
		For example, you would like to post a RealEsate listing on craigslist phoenix.
		Setup first the commands/info, sample below:

			info = {"price": "500,000",
					"sqft": "500",
					"bedroom" "4",
					"title": "500 sqft Condo in downtown phoenix RUSH",
					"sloc": "Some Avenue Corner 10th Street, Some City",
					"email": "myemail@gmail.com",
					"post": "I am selling my condo in Awesome Towers, its rush because I need the money. blah blah blah",
					"images": ['/home/Documents/Pictures/condo1.jpg', '/home/Documents/Pictures/condo2.jpg'],
					"re_type": "offer",
					"re_category": "re_owner",
					"ok_cats":"yes",
					"ok_dogs":"no",
					"privacy":"show"}

		ENCODE the above info as a VALID JSON. then run the code below on command line:
		python clposter.py phoenix housing_real_estate <encoded_json_string>
"""