from config import *
import logger
import record
import random
import sync
import os

avr = record.AV_Recorder()


while True:
	print('1. Start / Stop Recording')
	print('2. Cancel Recording')
	print('3. Sync to Server')
	print('4. ID-List of Sent Videos')
	print('5. Clear Database')
	print('6. Exit')
	ch = int(input())
	
	if ch == 1:
		if avr.is_recording():
			avr.stop()
			logger.new_log_entry(fname,avr.ext)
			print('Video was saved as "'+fname + '.' + avr.ext +'"\n')
		else:
			fname = 'vid' + str(random.randint(100,1001))
			avr.record(OUTPUT_DIR+fname)
			tt4.stop()
	elif ch == 2:
		avr.discard()
	elif ch == 3:
		sync.sync2server()
	elif ch == 4:
		sync.fetch_posted_questions()
	elif ch==5:
		os.system('rm -f %s'%DB_PATH)
	else:
		break

