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

imgs = ['"https://ja.gravatar.com/userimage/9847738/e0cfe4c445d28598ffc3d0a4fd235fa5.jpg?size=200"', \
  '"https://ja.gravatar.com/userimage/9847738/647f7900b8912b0669a1da2edc352b5e.jpg?size=200"',
  '"https://ja.gravatar.com/userimage/9847738/44b7b8d6b72f2dce6609be9e059c3920.jpg?size=200"']
html = '''
<head>
<title>GCP Control</title>
<link rel="icon" href={img}/>
<link rel="apple-touch-icon" href={img}/>
</head>
<body>
<p>
{body}
</p>
</body>
'''

project = 'wild-yukikaze'
zone = 'asia-northeast1-c'
def stop_all():
  instances = compute.instances().list(project=project, zone=zone).execute()
  for instance in instances['items']:
    name = instance.get('name')
    compute.instances().stop( project=project, zone=zone, instance=name).execute()
  print(html.format(body='finished all tear down', img=imgs[0]))

def start_all():
  instances = compute.instances().list(project=project, zone=zone).execute()
  for instance in instances['items']:
    name = instance.get('name')
    compute.instances().start( project=project, zone=zone, instance=name).execute()
  print(html.format(body='finished finished all start up', img=imgs[1]))

def check_ips():
  instances = compute.instances().list(project=project, zone=zone).execute()
  name_ip = {}
  for instance in instances['items']:
    #print(json.dumps(instance, indent=2) )
    name = instance['name']
    status = instance['status']
    networkIp = instance['networkInterfaces'][0]['networkIP']
    name_ip[name] = networkIp
    name_ip['status'] = status
  print(html.format(body=json.dumps(name_ip, indent=2), img=imgs[2]) )
 
#check_ips()
if args.get('ops') == 'start':
  start_all()
elif args.get('ops') == 'stop':
  stop_all()
elif args.get('ops') == 'ips':
  check_ips()
else:
  print('no operation specified.')
