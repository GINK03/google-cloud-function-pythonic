import os
import zipfile
import json
import uuid
import sys
import boto3
from pprint import pprint
from datetime import datetime, timezone, timedelta
from boto3.session import Session

ins = json.loads(input())
session = boto3.Session(
  aws_access_key_id='AKIAIXCQGQVC434OJILA',
  aws_secret_access_key=ins.get('secret'),
  region_name='ap-northeast-1',
)
ec2 = session.resource('ec2', region_name='ap-northeast-1')

response = session.client('ec2').describe_instances()
logs = []
for reserv in response["Reservations"]:
  #pprint(reserv, indent=2)
  instances = reserv.get('Instances')
  for instance in instances:
    tags = instance.get('Tags')
    state = instance.get('State')
    types = instance.get('InstanceType')
    log = {'tags':tags, 'state':state, 'types':types}
    logs.append(log)
#print( json.dumps(logs,indent=2,ensure_ascii=False))

jst_zone = timezone(timedelta(hours=+9), 'JST')
now = datetime.now(jst_zone).strftime('%Y-%m-%d_%H:%M:%S')
keyname = 'aws-machines-stats/machine_stat_{now}.json'.format(now=now)
obj = session.resource('s3').Object('cloud-status-stats', keyname)
body = json.dumps(logs,indent=2,ensure_ascii=False) 
obj.put(Body=bytes(body, 'utf8'))
print('ok')
