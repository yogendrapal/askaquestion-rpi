from config import *
import logger
import record
import random
import sync


avr = record.AV_Recorder()

while True:
	print('1. Start Recording')
	print('2. Stop Recording')
	print('3. Sync to Server')
	print('4. Exit')
	ch = int(input())
	
	if ch == 1:
		fname = 'vid' + str(random.randint(100,1001))
		avr.record(OUTPUT_DIR+fname)
	elif ch == 2:
		avr.stop()
		logger.new_log_entry(fname)
		print('Video was saved as "'+fname + '.mp4"\nPress any key to continue')
		input()
	elif ch == 3:
		sync.sync2server()
	else:
		break

