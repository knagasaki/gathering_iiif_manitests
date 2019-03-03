#!/usr/bin/env python3
# coding:utf-8
import urllib.request
import json
import sys
import re
wskey = sys.argv[1] 
keyword = sys.argv[2]
except_gallica = ''
if(3 in sys.argv):
 except_gallica = sys.argv[3]
skeyword = urllib.parse.quote(keyword)
wFilename = keyword+'_manilist.txt'
if except_gallica == 'exga':
 wFilename = keyword+'_exga_manilist.txt'  
wFile = open(wFilename, 'a')

def getUrl (wskey,skeyword,rows,start,eG):
  searchUrl = 'https://www.europeana.eu/api/v2/search.json?wskey='+wskey+'&query=sv_dcterms_conformsTo%3A%2Aiiif%2A&rows='+rows+'&start='+start+'&qf=title:%2A'+skeyword+'%2A'
  if eG == 'exga':
    searchUrl = searchUrl+'&qf=-PROVIDER%3ABiblioth%C3%A8que%2Anationale%2Ade%2AFrance'
  elif re.match('^-PROVIDER:', eG):
    searchUrl = searchUrl+'&qf='+eG
  readObj = urllib.request.urlopen(searchUrl)
  dataL = json.loads(readObj.read().decode('utf-8'))
  return(dataL)

data = getUrl(wskey,skeyword,"1","1",except_gallica)
maxNum = data["totalResults"]
print (str(maxNum)+' hit')
wFile.write(str(maxNum)+' hit\n')

for i in range(int(maxNum/100)+1):
 hi = str(i * 100 + 1)
 print (hi)
 dataE = getUrl(wskey,skeyword,"100",hi,except_gallica)
 recordBaseUrla = 'https://www.europeana.eu/api/v2/record'
 recordBaseUrlb = '.json?wskey='+wskey
 arImageUrls = []
 for item in dataE['items']:
   iid = item["id"]
   recordBaseUrl = recordBaseUrla+iid+recordBaseUrlb
   readObj2 = urllib.request.urlopen(recordBaseUrl)   
   recordData = json.loads(readObj2.read().decode('utf-8'))
   for eResource in recordData["object"]["aggregations"][0]["webResources"]:
      if "dctermsIsReferencedBy" in eResource:
   #["dctermsIsReferencedBy"]
        maniUrl = ','.join(eResource["dctermsIsReferencedBy"])
        print (maniUrl)
        wFile.write(maniUrl+'\n')
print ('finish')
wFile.close()
