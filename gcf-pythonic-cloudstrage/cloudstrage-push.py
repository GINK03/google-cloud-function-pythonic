import os
import zipfile
import json

try:
  obj = json.loads(input())
  z = zipfile.ZipFile('credentials.json.zip')
  z.extract('credentials.json', path='.', pwd=bytes(obj['secret'],'utf8') )
except Exception as ex:
  ...

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
#print('b', obj)
try:
  from google.cloud import storage
  client = storage.Client()
  # https://console.cloud.google.com/storage/browser/[bucket-id]/
  bucket = client.get_bucket('wired-ant')
  # Then do other things...
  blob = bucket.get_blob('a.txt')
  print(blob.download_as_string().decode('utf8'))
except Exception as ex:
  print(ex)
#blob.upload_from_string('New contents!')
#blob2 = bucket.blob('remote/path/storage.txt')
#blob2.upload_from_filename(filename='/local/path.txt')

