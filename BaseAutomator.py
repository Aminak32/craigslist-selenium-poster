#!/usr/bin/env python

""" Craigslist poster application using selenium API
	Base class for all other Automation Modules
	@author Ivan Dominic Baguio - baguio.ivan@gmail.com """

import sys, json, random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from time import sleep

class BaseAutomator():
	def __init__(self, baseUrl, commandStr, driver="firefox", verbose=False, dont_close=False):
		self.verbose = verbose
		self.dont_close = dont_close
		self.test = "Hello World"
		if self.verbose:
			print "Initializing %s automator" %(self.automator_name)
			print "Base url:",baseUrl
			print "Will be using", driver, "as webdriver"
	
		try:
			if driver == "chrome":
				self.driver = webdriver.Chrome()
			else:
				self.driver = webdriver.Firefox()
		except Exception, e:
			print e
			sys.exit(0)

		self.loadCommands(commandStr)						#loads the commands from JSON, see docu below
		self.baseUrl = baseUrl

	def automate(self):
		"""Main automation method that must be overidden"""
		#go to base url
		if self.verbose: print "Loading %s page..." %(self.automator_name)
		self.driver.get("https://"+self.baseUrl+self.address)

		if self.verbose: print "Clicking post url"
		xpath="""//*[@id="ef"]/a[2]"""						#the xpath of the post btn/link.
		btn = self.driver.find_element_by_xpath(xpath)
		btn.click()

	def uploadImages(self):
		if self.verbose: print "Uploading images..."
		print self.commands['images']
		for img in self.commands['images']:
			if self.verbose: print "Uploading ",img
			inpt = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, self.upload_xpath)))
			inpt.send_keys(img)
			sleep(1)

	def finish(self):
		"""Do finishing stuffs"""
		if self.verbose: print "Finalizing post..."
		btn = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, self.done_xpath)))
		btn.click()

		if self.verbose: print "Publishing post..."
		btn = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, self.publish_xpath)))
		btn.click()

		if not self.dont_close:
			if self.verbose: print "Quiting browser..."
			self.driver.quit()

"""DOCUMENTATION for BaseAutomator
	BaseAutomator is the base class that is extended by specific automators
	it contains the basic methods that are used by all automators.

	Running the Automator
	1. run clposter.py <location> <category> <json of commands>
	2. optionally you may include the -v argument to increase verbosity

	<location>
		the subdomain of Craigslist you want to post. See all_locations.json for valid list
	<category>
		the specific category in Craigslist that the post will be posted. See each categories
		documentation for more information
	<json of commands and info >
		commands and info that will be used by the automator in posting the listing. Must be
		in JSON dict format

	REQUIRED BASE COMMANDS:
		KEY			DESCRIPTION
		subloc 		sublocation of the current location, if not included, randomize
		title 		title of the listing
		sloc 		specific location
		email 		reply to email of the listing
		post 		main description of the listing
		images 		list of image paths, max 8

	OPTIONAL BASE COMMANDS:
		ok_contact	check OK contact
"""