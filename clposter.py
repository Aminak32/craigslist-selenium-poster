#!/usr/bin/env python

""" Craigslist poster application using selenium API
	main script - basically manages the command line arguments
	@author Ivan Dominic Baguio - baguio.ivan@gmail.com """

import argparse, sys, json
from RealEstateAutomator import RealEstateAutomator
from ServicesAutomator import ServicesAutomator

"""Setting up the command line arguments"""
parser = argparse.ArgumentParser(description="Command line python script that posts to craigslist using selenium API")

"""Required arguments"""
#location/city where the ad would be posted
parser.add_argument("location", help="craigslist location subdomain, <location>.craigslist.org")
#category where the item would be posted
parser.add_argument("category", help="category where the item will be posted")
parser.add_argument("commands", help="command string that will be passed to respective automator")
#optional arguments
parser.add_argument("-v","--verbose",help="print stuffs to stdout", action="store_true")
parser.add_argument("-b","--browser", help="choose which browser to use", choices=["chrome","firefox"], default="firefox")
parser.add_argument("-d","--dont_close", help="dont close the browser window after posting is finished", action="store_true")

cli_args = parser.parse_args()

#global variables
verbose = False
base_url = ""
dont_close = False

def main():
	global verbose, base_url, dont_close
	verbose = cli_args.verbose
	if verbose: print "Verbose mode turned ON"
	if verbose and dont_close: print "Will not close window after posting is completed"
	base_url = getLocationURL(cli_args.location)
	dont_close = cli_args.dont_close
	validCategory(cli_args.category)
	runCategory(cli_args.category)

def getLocationURL(location):
	"""Checks if the input location is valid, and returns the base URL for that city
	returns none if invalid location. see all_locations.json for a list of valid
	locations/cities"""

	if verbose: print "getting location url for:",location
	locs_file = None
	try:
		fname = "json_files/all_locations.json"
		with open(fname,"r") as locs_file:
			d = json.loads(locs_file.read())
			if verbose: print "Location base url:",d[location]
			return d[location]
	except Exception as e:
		print fname,"file cannot be found. Will exit"
		print e
		sys.exit(0)

def validCategory(category):
	"""Checks if the input category is valid, returns the url of the category if valid
	returns none if invalid category. see all_sub_url.json for a list of valid categories"""

	if verbose: print "getting category url for:",category
	try:
		fname = "json_files/all_sub_url.json"
		with open(fname,"r") as sub_url_file:
			d = json.loads(sub_url_file.read())
			if verbose: print "Category url:",d[category]
			return d[category]

	except Exception as e:
		print fname,"file cannot be found. Will exit"
		print e
		sys.exit(0)

def runCategory(category):
	if verbose: print "Running automator for:",category
	if category == "housing_real_estate":
		re_automator = RealEstateAutomator(base_url, cli_args.commands, driver = cli_args.browser, verbose = verbose, dont_close=dont_close)
		re_automator.automate()
	if category.startswith("service_"):
		serv_automator = ServicesAutomator(base_url, cli_args.commands, category,driver = cli_args.browser, verbose = verbose, dont_close=dont_close)
		serv_automator.automate()

if __name__ == "__main__":
	main()