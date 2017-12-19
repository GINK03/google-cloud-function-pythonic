import os
import zipfile
import json
import uuid
import sys
import boto3
from pprint import pprint
from datetime import datetime, timezone, timedelta
jst_zone = timezone(timedelta(hours=+9), 'JST')
from boto3.session import Session

ins = json.loads(input())
session = boto3.Session(
  aws_access_key_id='AKIAIXCQGQVC434OJILA',
  aws_secret_access_key=ins.get('secret'),
  region_name='ap-northeast-1',
)
resource = session.resource('cloudwatch', region_name='ap-northeast-1')
cloud_watch = session.client('cloudwatch')
metrix = cloud_watch.list_metrics()
#pprint(metrix)

# make dimentions 
dimentions = []
for dim in metrix.get('Metrics'):
  dimention = dim.get('Dimensions')

  # need to unbox
  if dimention == []:
    continue
  if dimention[0].get('Name') != 'InstanceId':
    continue
  # need to unbox
  dimentions.append( dimention[0] )

network = {'networkIn': 0.0, 'networkOut':0.0}

for (INOUT, METRIX) in [('networkIn', 'NetworkIn'), ('networkOut', 'NetworkOut')]:
  for i in range(0, len(dimentions) - 10, step=10):
    net_in_stat = cloud_watch.get_metric_statistics( Namespace='AWS/EC2', MetricName=METRIX, 
                            Dimensions=dimentions[i:i+10],
                            StartTime=datetime.now(jst_zone) - timedelta(days=1),
                            EndTime=datetime.now(jst_zone),
                            Period=3600*24,
                            Statistics=['Average'])
    datapoint = net_in_stat.get('Datapoints')
    if datapoint == []:
      continue
    # need unbox
    average = datapoint[0].get('Average')
    average = average * len(dimentions[i:i+10]) # multiply chunk size
    #pprint(net_in_stat, indent=2)
    network[INOUT] += average

now = datetime.now(jst_zone).strftime('%Y-%m-%d_%H:%M:%S')
keyname = 'aws-network-stats/network_stats_{now}.json'.format(now=now)
obj = session.resource('s3').Object('cloud-status-stats', keyname)
body = json.dumps(network,indent=2,ensure_ascii=False) 
obj.put(Body=bytes(body, 'utf8'))
print('ok')
