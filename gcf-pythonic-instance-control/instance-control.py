import os
import zipfile
import json
import uuid
import sys
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
raw = input()
try:
  ...
except Exception as ex:
  print(ex)

from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()
