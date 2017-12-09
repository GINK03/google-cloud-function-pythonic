import os
import zipfile
import json

try:
  obj = json.loads(input())
except:
  ...
try:
  os.system('sh ./gcs_mount.sh 2>&1 > /dev/null')
  #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
  os.environ['PATH'] = './usr/bin/mecab:%s'%os.environ['PATH'] 
  if os.environ.get('LD_LIBRARY_PATH') is not None:
    os.environ['LD_LIBRARY_PATH'] = './usr/lib:%s'%os.environ['LD_LIBRARY_PATH']
  else: 
    os.environ['LD_LIBRARY_PATH'] = './usr/lib'

  import MeCab

  m = MeCab.Tagger('-Owakati -d ./nardtree-nlp-dicts/mecab-ipadic-neologd')

  wakati = m.parse('艦これとアズールレーンとアルペジオ').strip()
  print(wakati)
except Exception as ex:
  print(ex)
