#!/usr/bin/env python

import json, os, sys, argparse, urllib2
from time import sleep
from myhttplib import getPage
from ServiceAutomator import ServiceAutomator

verbose = True
"""Setting up the command line arguments"""
parser = argparse.ArgumentParser(description="Command line python script that posts to craigslist using selenium API")

"""Required arguments"""
#optional arguments
parser.add_argument("-i","--ip_address", help="ip address of host", default="64.187.124.250")
parser.add_argument("-p","--port", help="port number to connect", default="400")
parser.add_argument("-v","--verbose",help="print stuffs to stdout", action="store_true")
parser.add_argument("-b","--browser", help="choose which browser to use", choices=["chrome","firefox"], default="firefox")
parser.add_argument("-d","--dont_close", help="dont close the browser window after posting is finished", action="store_true")

cli_args = parser.parse_args()
poster_address = None

def main():
  global verbose, poster_address
  poster_address = cli_args.ip_address + ":" + cli_args.port
  dialer_proxy = getProxy()
  get_post_url = "http://%s/ws.php?action=get_schedule"%(poster_address)
  post_json = json.loads(getPage(get_post_url,verbose))

  for commands in post_json['schedules']:
    if len(sys.argv)==1:
      mac_chnge_url = "http://%s/start_dialup.php?macaddr=%s" %(dialer_proxy['ip'],commands['mac'])
    else:
      mac_chnge_url = "http://%s/start_dialup.php?macaddr=%s" %(dialer_proxy['ip'],sys.argv[1])
    if verbose: print "Requesting mac change on",mac_chnge_url
    #if getPage(mac_chnge_url, verbose) == "1": print "Okay from server"
    for i in range(6):
      if verbose: print "%d seconds to wait..."%((6-i)*30)
      sleep(30) #sleep 3mins
    new_proxy = getProxy()
    if new_proxy['ip'] != dialer_proxy['ip']:
      if verbose: print "Old and New proxy has changed\nDo stuff with CL NOW"

    location = "miami"
    verbose = True
    base_url = "miami.craigslist.org"
    proxy_ = new_proxy['ip']+":"+new_proxy['port']

    img_path = loadImages(commands['image'], commands['image_filename'], verbose=True)
    commands['images'] = [img_path]
    commands['poster_address'] = poster_address

    serv_automator = ServiceAutomator(base_url, commands, browser=cli_args.browser, verbose=verbose, dont_close=True, proxy=proxy_)
    serv_automator.automate()

#downloads the image from img_url and returns path of file
def loadImages(img_url, img_fname, verbose=False):
    if verbose: print "Downloading image from:", img_url
    temp = 'tmp/'
    if not os.path.exists(temp):
      if verbose: print "Creating new temp folder"
      os.makedirs(temp)

    img = urllib2.urlopen(img_url)
    with open(temp+img_fname,"wb") as file_:
      file_.write(img.read())
      if verbose: print "File downloaded. Saved to:", file_.name
      return os.path.realpath(__file__)+"/"+file_.name

def getProxy():
	get_dialer_url = "http://%s/ws.php?action=get_dialer_ip" %(poster_address)
	return json.loads(getPage(get_dialer_url,verbose))

if __name__ == "__main__":
	main()