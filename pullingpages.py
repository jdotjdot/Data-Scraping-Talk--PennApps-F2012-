# Grabbing a simple page using requests

import requests

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
	r = requests.post('http://www.mysite.com/login',
			params={'username': 'jj', 'password': 'PlaintextPasswordsAreBad'})
	return r

def pretend_we_are_chrome():
	# Can this make a difference when pulling webpages?  Absolutely.

	CHROME_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

	r = requests.get('http://www.whatismybrowser.com/',
			headers={'user-agent': CHROME_USER_AGENT})

	#if we want to get the text instead:
	return r.text
