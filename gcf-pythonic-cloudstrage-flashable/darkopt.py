import sys
import os

import uuid

random = '%s'%uuid.uuid4()
q = 'curl -X POST -H "Content-Type:application/json" -d \'{"secret":"%s"}\' https://us-central1-machine-learning-173502.cloudfunctions.net/pycall_gcs?secret_get=%s'%(random,random)
print(q)
for i in range(1000):
  os.popen(q)

