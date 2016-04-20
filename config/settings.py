NEMOPAY_API_URL = 'https://api.nemopay.net/'
NEMOPAY_SYSTEM_ID = 'payutc'
NEMOPAY_API_KEY = ''
NEMOPAY_LOGIN_SERVICE = 'TRESO'
NEMOPAY_CONNECTION_UID = ''
NEMOPAY_CONNECTION_PIN = ''

try:
	from config.local_settings import *
except ImportError:
	pass
