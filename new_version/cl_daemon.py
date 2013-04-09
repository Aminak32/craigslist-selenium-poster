#!/usr/bin/env python

import argparse, threading
from postGetter import postMain
from time import sleep

"""Setting up the command line arguments"""
parser = argparse.ArgumentParser(description="Command line python script that posts to craigslist using selenium API")

"""Required arguments"""
#optional arguments
parser.add_argument("-i","--ip_address", help="ip address of host", default="64.187.124.250")
parser.add_argument("-p","--port", help="port number to connect", default="400")
parser.add_argument("-v","--verbose",help="print stuffs to stdout", action="store_true")
parser.add_argument("-b","--browser", help="choose which browser to use", choices=["chrome","firefox"], default="firefox")
parser.add_argument("-d","--dont_close", help="dont close the browser window after posting is finished", action="store_true")
parser.add_argument("-r","--records",help="number of records to get from server",type=int, default=1)
parser.add_argument("-n","--no_proxy", help="disable the use of proxy", action="store_true")
parser.add_argument("-t","--delay",help="time delay before each post run (in seconds)", default=800)

cli_args = parser.parse_args()
def main():	
	if cli_args.verbose: print "Starting daemon..."
	while True:
		t = threading.Thread(target=callPoster)
		t.daemon = True
		t.start()
		sleep(cli_args.delay)

def callPoster():
	if cli_args.verbose: print "Creating new thread and starting post script..."
  	poster_address = cli_args.ip_address + ":" + cli_args.port
  	postMain(poster_address, cli_args.browser, cli_args.records, cli_args.dont_close,cli_args.no_proxy, verbose=cli_args.verbose)

if __name__ == "__main__":
	main()