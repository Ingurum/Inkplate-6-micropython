# Copy this file and rename it to `config.py`

# OAuth2 Configuration
# Look at: https://developers.google.com/identity/protocols/oauth2/limited-input-device

API_KEY = '<your_api_key'
CLIENT_ID = '<your_client_id>'
CLIENT_SECRET = '<your_client_secret>'
DISCOVERY_ENDPOINT = 'https://accounts.google.com/.well-known/openid-configuration'

# The  list of OAuth2 scopes. 
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# The location for auth state serialization and deserialization.
SAVED_LOCATION =  'tokens.json'

# Wireless Config
WLAN_SSID = '<your_ssid>'
WLAN_PASSWORD = '<your_password>'

# Time Zone Configuration
UTC_OFFSET = -8.0

# Deep sleep interval in minutes
REFRESH_INTERVAL = 10