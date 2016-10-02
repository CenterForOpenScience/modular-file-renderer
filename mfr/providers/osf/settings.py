from mfr import settings

config = settings.child('OSF_PROVIDER_CONFIG')

# BASE_URL = config.get('BASE_URL', 'http://localhost:5001/')

MFR_IDENTIFYING_HEADER = config.get('MFR_IDENTIFYING_HEADER', 'X-Cos-Mfr-Render-Request')
