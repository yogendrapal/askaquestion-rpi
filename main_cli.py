from config import *
import logger
import record
import random


avr = record.AV_Recorder()

while True:
	print('1. Start Recording')
	print('2. Stop Recording')
	print('3. Sync to Server')
	print('4. Exit')
	ch = int(input())
	fname = 'vid' + str(random.randint(100,1001))
	if ch == 1:
		avr.record('output/'+fname)
	elif ch == 2:
		avr.stop()
		logger.new_log_entry(avr.output_name)
		print('Video was saved as "'+avr.output_name + '.mp4"\nPress any key to continue..')
		input()
	else:
		break

