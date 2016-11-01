from mfr import settings


config = settings.child('OSF_PROVIDER_CONFIG')

MFR_IDENTIFYING_HEADER = config.get('MFR_IDENTIFYING_HEADER', 'X-Cos-Mfr-Render-Request')
