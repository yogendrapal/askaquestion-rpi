import json
from datetime import datetime
from config import *


# log_db = {
# 	'vidname':'temp.mp4',
# 	'date':'',
# 	'time':'',
# 	'machine_id':''
# }


'''
useful links

https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
https://www.programiz.com/python-programming/datetime/current-datetime

'''

def new_log_entry(filename):
	now = datetime.now()
	ldb = {}
	ldb['name'] = filename
	ldb['date'] = now.strftime("%d/%m/%y")
	ldb['time'] = now.strftime("%H:%M:%S")
	ldb['machine_id'] = MACHINE_ID

	#add the json extension
	jsonfile = filename + '.json'
	vidname=filename+ '.mp4'
	with open(OUTPUT_DIR+jsonfile,'w+') as outfile:
		json.dump(ldb,outfile)
	
	
	return
