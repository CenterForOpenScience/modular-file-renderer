from mfr import settings


config = settings.child('OSF_PROVIDER_CONFIG')

MFR_IDENTIFYING_HEADER = config.get('MFR_IDENTIFYING_HEADER', 'X-Cos-Mfr-Render-Request')
MFR_ACTION_HEADER = config.get('MFR_ACTION_HEADER', 'X-Cos-Mfr-Request-Action')
