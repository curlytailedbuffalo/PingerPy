from Pinger import Pinger
import json
import urllib2
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('debug.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
logger.info("Starting PingerPy")

storage_file = "../settings/config.json"


while True:
	poll_interval = 300
	try:
		data = json.load(open(storage_file))
	except:
		data = False
	
	enabled = True
	if data != False:
		if not 'settings' in data or not 'storage' in data:
			logger.info("Couldn't find base settings or storage in the json file")
			enabled = False
		else:
			if not 'access_token' in data['settings'] or not 'api_url' in data['settings'] or not 'app_id' in data['settings'] or not 'poll_interval' in data['settings']:
				logger.info("There is an issue with your settings in the json file")
				enabled = False

	
	if enabled == True:
		
		# Will need to format the list differently for the Pinger class
		host_list = []
		logger.info("Getting host list from JSON storage... %s", data)
		api_url = data['settings']['api_url'] + data['settings']['app_id'] + '/statechanged/'
		
		for (i, item) in enumerate(data['storage']):
			host_list.append(item)

		poll_interval = 60 * 60
		if int(data['settings']['poll_interval']) > 1:
			poll_interval = int(data['settings']['poll_interval']) * 60

		logger.info("Starting watchdog, poll interval set to %s minutes / %s seconds",  data['settings']['poll_interval'], poll_interval)

		ping = Pinger()
		# How many IPs will be tested at same time
		ping.thread_count = 8
		ping.hosts = host_list

		
		logger.info("Pinging IPs...")
		# Checks IPs and returns a dict of dead and alive hosts
		msg = ping.start()


		for device in msg['alive']:
			if data['storage'][device] == "offline":
				logger.info("Change in state detected: %s off -> on...", device)
				
				outbound_url = api_url + "online?access_token=" + data['settings']['access_token'] + "&ipadd=" + device
				req = urllib2.Request(outbound_url)
				try:
					response = urllib2.urlopen(req)
					data['storage'][device] = "online"
					logger.info("Update was a success - Device: %s, New Value: On", device)
				except URLError, e:
					logger.info("Update to Smartthings failed - device: %s, error_code: $s, error_message: %s", device, e.code, e.read())

				
				
				
		for device in msg['dead']:
			
			if data['storage'][device] == "on":
				logger.info("Change in state detected: %s on -> off...", device)
				outbound_url = api_url + "offline?access_token=" + data['settings']['access_token'] + "&ipadd=" + device
				try:
					response = urllib2.urlopen(req)
					data['storage'][device] = "offline"
					logger.info("Update was a success - Device: %s, New Value: Off", device)
				except URLError, e:
					logger.info("Update to Smartthings failed - device: %s, error_code: $s, error_message: %s", device, e.code, e.read())
					
				if response.code == 200 or response.code == "200":
					data['storage'][device] = "online"
					logger.info("Update was a success - Device: %s, New Value: Off", device) 
				else:
					logger.error("Smartthings update request failed", device)
			
		with open(storage_file, 'w') as outfile:
			json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
			outfile.close()
			outfile = None;
		 

	logger.info("Sleeping...")
	time.sleep(poll_interval)
else:
	logger.info("No configuration file found, quiting")
