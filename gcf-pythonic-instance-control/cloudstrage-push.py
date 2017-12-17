import os
import zipfile
import json
import uuid
import sys
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
raw = input()
try:
  from google.cloud import storage
  from google.cloud.storage import Blob
  client = storage.Client()
  bucket = client.get_bucket('wired-ant')
  print(bucket, file=sys.stderr)
  uuid = '%s.shard'%uuid.uuid4()
  blob = bucket.get_blob(uuid)
  if blob is None:
    print(blob, file=sys.stderr)
    blob = Blob(uuid, bucket)
    source = ''
  else:
    source = blob.download_as_string().decode()
  blob.upload_from_string( source + raw + '\n', content_type='text/plain')
except Exception as ex:
  print(ex)
