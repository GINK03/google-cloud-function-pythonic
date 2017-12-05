import concurrent.futures

import os

import json
ipaddrs = []
def _map1(arr):
  ipaddr = os.popen('curl -s https://us-central1-machine-learning-173502.cloudfunctions.net/shotgun').read()
  print('ipaddr', arr, ipaddr.strip())
  ipaddrs.append(ipaddr.strip())
  return ipaddr

arrs = [i for i in range(1024)]
with concurrent.futures.ThreadPoolExecutor(max_workers=1024) as exe:
  exe.map(_map1, arrs)

open('ipaddrs.json', 'w').write( json.dumps(ipaddrs, indent=2) )
