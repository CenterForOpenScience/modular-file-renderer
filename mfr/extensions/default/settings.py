from mfr import settings

config = settings.child('CODEPYGMENTS_EXTENSION_CONFIG')

MAX_SIZE = int(config.get('MAX_SIZE', 204800))  # 200kb

lexer_lib = {
    '.gdt': 'xml',
    '.pzfx': 'xml',
    '.cmdi': 'xml',
    '.rm5': 'xml',
    '.eaf': 'xml',
    '.qsf': 'json',
    '.psyexp': 'html',
    '.umbrella': 'json',
    '.jst': 'js',
    '.ijm': 'java',
    '.csl': 'xml',
    '.lss': 'xml'
}
