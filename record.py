import shlex
from subprocess import Popen, DEVNULL, STDOUT
import os
from config import *

'''
final command sample

ffmpeg -y -f alsa -i default -f v4l2 -i /dev/video0 -acodec aac -strict -2 -ac 1 -b:a 64k -vcodec libx264 -b:v 300k -r 30 -g 30 output/vid838.mp4

'''

class AV_Recorder():

	def __init__(self):
		
		self.video_device = 0
		self.num_audio_channels = 1
		if LOW_SETTING:
			self.ext = 'avi'
		else:
			self.ext = 'mp4'

		self.cmd = 'ffmpeg'
		#record audio using alsa, use the default recording device
		self.rec_audio_cmd = ' -f alsa -i default'
		
		self.rec_video_v4l2 = ' -f v4l2 -i /dev/video%d' % self.video_device
		#audio codec for v4l2 (codec is aac, bitrate is 64k)
		self.rec_video_acodec = ' -acodec aac -strict -2 -ac %d -b:a 64k' % self.num_audio_channels
		#video codec for v4l2
		if LOW_SETTING:
			self.rec_video_vcodec = ' -r 25 -s 640x480 -qscale:v 1'
		else:
			self.rec_video_vcodec = ' -vcodec libx264 -b:v 300k -r 30 -g 30'
		#record video command
		if RECORD_VIDEO_ONLY:
			self.rec_video_cmd = self.rec_video_v4l2 + self.rec_video_vcodec
		else:
			self.rec_video_cmd = self.rec_video_v4l2 + self.rec_video_acodec + self.rec_video_vcodec
		#output filename
		self.output_name = 'temp_output'
		self.output_cmd = ' -f tee "output.mp4|[f=nut]pipe:" | ffplay pipe:'
		#Popen object will be stored in pff
		self.pff = None
		
	def is_recording(self):
		if self.pff:
			return True
		else:
			return False

	def generate_output_cmd(self):
		self.output_cmd = ' %s' % (self.output_name + '.' + self.ext)

	def generate_cmd(self):
		#final recording command for video and audio recording with ffmpeg
		self.generate_output_cmd()
		if RECORD_VIDEO_ONLY:
			self.cmd = 'ffmpeg -y' + self.rec_video_cmd + self.output_cmd
		else:
			self.cmd = 'ffmpeg -y' + self.rec_audio_cmd + self.rec_video_cmd + self.output_cmd

	def record(self,filename):
		self.output_name = filename
		self.generate_cmd()
		print('\n--ffmpeg command--\n',self.cmd,'\n')
		self.pff = Popen(shlex.split(self.cmd), stdin = DEVNULL, stdout = DEVNULL, stderr = STDOUT)
		print('recording started...\n')

	def stop(self):
		self.pff.terminate()
		self.pff = None
		print('recording stopped.\n')

	def discard(self):
		if self.pff:
			self.pff.terminate()
			os.system('rm -f %s'%(self.output_name + '.' + self.ext))
			self.pff = None
			print('recording discarded.\n')
		else:
			print('No active recording!\n')
