# function called by the API
import json
import requests
import time
import datetime
import os
import csv
import random
import sys
import traceback
import threading
import zipfile
import re
import copy

BASISURL="https://entscheidsuche.ch/docs"

TEMPLATEKEYS=["URL","ID","text","exclude","title","type","source.name","source.logo","editors","authors","abstract","date","restart"]
Status={}
reNum=re.compile("BGE\s+\d+\s+[A-Z]+\s\d+")
query_body={"size":20,"_source":{"excludes":["attachment.content"]},"track_total_hits":True,"query":{"bool":{"must":{"query_string":{"query":"","default_operator":"AND","type":"cross_fields","fields":["title.*^5","meta.*^10"]}}}},"sort":[{"_score":"desc"},{"id":"desc"}]}
query_url="https://entscheidsuche.pansoft.de:9200/entscheidsuche-*/_search"
query_header={ "content-type": "application/json"}

def parse(sdata):
	print("search:",sdata)
	p={ a: "" for a in TEMPLATEKEYS}
	reply={}
	reply['status']='ok'
	for i in sdata:
		if i in p:
			p[i]=sdata[i]
		else:
			reply['warning']="Unknown parameter "+i
			reply['status']="error"			
	if reply['status']=='ok':
		match=reNum.findall(p['text'])
		if match:
			reply['message']="gefunden: "+", ".join(match)
			links={}
			reply['dump']=""
			for i in match:
				if not i in links:
					adapted_body=query_body
					adapted_body['query']['bool']['must']['query_string']['query']="\""+i+"\""
					response=requests.post(url=query_url, headers=query_header, data=json.dumps(adapted_body), verify=False)
					reply['dump']+="..."+response.text
					
			
	return reply

