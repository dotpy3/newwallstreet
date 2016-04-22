NEMOPAY_API_URL = 'https://api.nemopay.net/services/'
NEMOPAY_SYSTEM_ID = 'payutc'
NEMOPAY_API_KEY = ''
NEMOPAY_LOGIN_SERVICE = 'GESARTICLE'
NEMOPAY_CONNECTION_UID = ''
NEMOPAY_CONNECTION_PIN = ''

BEER_CATEGORIES = [10, 11]

try:
	from config.local_settings import *
except ImportError:
	pass
