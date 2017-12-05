import os

import zipfile

z = zipfile.ZipFile('credentials.json.zip')
z.extract('credentials.json', path='.', pwd=bytes('91nk9003','utf8') )
