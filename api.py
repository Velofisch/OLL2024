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
	return reply

