#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import logging
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('debug.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

PORT_NUMBER = 9092

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		logger.info("Receiving GET request...")
		
		data = self.get_settings_file()
		
		if data == False:
			self.return_error('Could not find your JSON configuration file.')
			return
			
			
		if self.path=="/setup":
			self.path="/setup.html"
			
		elif self.path=="/config":
			html = '<head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>PingerPy - Current Config</title></head>'
			html += '<h2>Current configuration:</h2><a href="/setup" target="_parent" title="Edit Configuration">edit</a>'
			for key in data:
				html += '<h3>' + key + '</h3>'
				html += '<ul>'
				for c in data[key]:
					
					html += '<li>' + c + ' = ' + json.dumps(data[key][c]) + '</li>'

				html += '</ul>'
			self.return_error("" + html )
		
		else:
			if not 'settings' in data or not 'storage' in data:
				logger.info("Redirect - Starting intial setup")
				self.redirect_page('setup')
				return
			if not 'access_token' in data['settings'] or not 'api_url' in data['settings'] or not 'poll_interval' in data['settings']:
				logger.info("Redirect - Starting intial setup")
				self.redirect_page('setup')
				return

			if self.path=="/":
				self.path="/index.html"
			
		self.process_html_page()
		
		return

	#Handler for the POST requests
	def do_POST(self):
		
		logger.info("Receiving POST request...")
		
		data = self.get_settings_file()
		
		if data == False:
			self.return_error('Could not find your JSON configuration file.')
			return

			
		if self.path=="/add":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
			if not 'new_ip' in form:
				self.return_error('No IP Provided')
				return
			new_ip = form['new_ip'].value
			logger.info("Request is Add New IP, IP is: %s", new_ip)
			
			data['storage'][new_ip] = "offline"
			logger.info("Saving new IP to file...")
			self.save_settings_file(data)
			
			self.redirect_page('/')
			
		elif self.path=="/setup-complete":
			data = {
				'settings' : {},
				'storage' : {}
			}
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
			if not 'setup_appid' in form or not 'setup_accesstoken' in form or not 'setup_endpointurl' in form or not 'setup_pollinterval' in form:
				self.return_error('Make sure to completely fill out the intial setup form and try again')
				return

			logger.info("New settings data received")
			
			data['settings']['access_token'] = form['setup_accesstoken'].value
			data['settings']['app_id'] = form['setup_appid'].value
			data['settings']['api_url'] = form['setup_endpointurl'].value
			data['settings']['poll_interval'] = form['setup_pollinterval'].value
			
			logger.info("Saving new IP to file...")
			self.save_settings_file(data)
			
			self.redirect_page('/')
		else:
			self.redirect_page('/')
			
		return		
	
	def get_settings_file(self):
		storage_file = "../settings/config.json"
		try:
			return json.load(open(storage_file))
		except:
			return False
	
	def save_settings_file(self, data):
		storage_file = "../settings/config.json"
		with open(storage_file, 'w') as outfile:
			json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
			outfile.close()
			outfile = None;
	
	def process_html_page(self):
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
	
	
	def redirect_page(self, redirect):
		self.send_response(301)
		self.send_header('Location',redirect)
		self.end_headers()
	
	def return_error(self, message):
		
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(message)
		return
		
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	logger.info('Started httpserver on port %s' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	logger.info('^C received, shutting down the web server')
	server.socket.close()
