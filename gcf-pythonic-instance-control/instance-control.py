import os
import zipfile
import json
import uuid
import sys
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
try:
  raw = input()
  args = json.loads(raw)
except Exception as ex:
  print(ex)

from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

from googleapiclient import discovery
compute = discovery.build('compute', 'v1', credentials=credentials)

project = 'wild-yukikaze'
zone = 'asia-northeast1-c'
def stop_all():
  instances = compute.instances().list(project=project, zone=zone).execute()
  for instance in instances['items']:
    name = instance.get('name')
    compute.instances().stop( project=project, zone=zone, instance=name).execute()
  print('finished')

def start_all():
  instances = compute.instances().list(project=project, zone=zone).execute()
  for instance in instances['items']:
    name = instance.get('name')
    compute.instances().start( project=project, zone=zone, instance=name).execute()
  print('finished')

if args.get('ops') == 'start':
  start_all()
elif args.get('ops') == 'stop':
  stop_all()
else:
  print('no operation specified.')
