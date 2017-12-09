import os
import zipfile
import json

try:
  obj = json.loads(input())
except:
  ...
#try:
os.system('sh ./gcs_mount.sh  > /dev/null')
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'
PWD=os.environ['PWD']
os.environ['PATH'] = PWD + '/local/bin/mecab:%s'%os.environ['PATH'] 
os.environ['LD_LIBRARY_PATH'] = os.getcwd()
import MeCab
mecabrc = PWD + '/local/etc/mecabrc'
m = MeCab.Tagger('-Owakati -d ./nardtree-nlp-dicts/mecab-ipadic-neologd -r ' + mecabrc)

wakati = m.parse('艦これとアズールレーンとアルペジオ').strip()
print(wakati)
#except Exception as ex:
#  print("Exception", ex)
