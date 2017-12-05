import sys

import requests
import bs4
import numpy as np

r = requests.get('http://www.ugtop.com/spill.shtml')
r.encoding = r.apparent_encoding
#print( r.text )

soup = bs4.BeautifulSoup(r.text)
ipaddr = soup.find('font', {'color':'blue', 'size':'+2'})
print(ipaddr.text)
