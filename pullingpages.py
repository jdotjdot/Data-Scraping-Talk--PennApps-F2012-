# Grabbing a simple page using requests

# with requests, "params" are for GET--the querystring args
#				 "data" is for POST--the form information

# This code can be considered part of the public domain, for any use by anyone.

import requests
import re
from bs4 import BeautifulSoup

def simple_get():
	r = requests.get('http://www.upenn.edu/registrar/register/')
	return r

def get_with_bakedin_url(course_code):
	r = requests.get('http://www.upenn.edu/registrar/register/%s.html' % course_code)
	# the above returns something like http://www.upenn.edu/registrar/register/acct.html
	return r

# Let's do a google search!
def get_with_get_params():
	r = requests.get('http://www.google.com/search', params={'q': 'hiya'})
	# this actually requests http://www.google.com/search?q=hiya
	return r

def post_request():
	# this is just an example and doesn't do anything
	r = requests.post('http://www.mysite.com/updateinfo',
			data={'username': 'jj', 'password': 'PlaintextPasswordsAreBad',
					'address': '3901 Locust Walk'})
	return r

def pretend_we_are_chrome():
	# Can this make a difference when pulling webpages?  Absolutely.

	CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

	r = requests.get('http://www.whatismybrowser.com/',
			headers={'user-agent': CHROME_USER_AGENT})

	#if we want to get the text instead:
	return r.text

def login_and_stay_logged_in():
	# Using this piece of the requests module allows you to maintain cookies
	# and sessions (including authentication) across multiple requests, which
	# basically allows you to log into a website and stay logged in in order to
	# pull your information.

	# https://secure.westelm.com/account/login.html

	username = 'pennapps@suremail.info'
	password = 'pennapps1'

	s = requests.session(headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.10 (KHTML, like Gecko) Chrome/23.0.1263.1 Safari/537.10'})

	r = s.get('https://secure.westelm.com/account/login.html')

	r = s.post('https://secure.westelm.com/authenticate.html',
				data={'email': username,
						'password': password,
						'x': 0, 'y': 0},
						# How do I know about 'x' and 'y'?
						# From viewing the headers in the POST
						# request using Chrome's developer tools
						# That being said, might not be necessary
				headers={'referer': 'https://secure.westelm.com/account/login.html',
						 'origin': 'https://secure.westelm.com',
						 })


	return s