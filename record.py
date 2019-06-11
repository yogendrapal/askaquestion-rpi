import shlex
from subprocess import Popen, DEVNULL, STDOUT
from config import *

'''
final command sample

ffmpeg -y -f alsa -i default -f v4l2 -i /dev/video0 -acodec aac -strict -2 -ac 1 -b:a 64k -vcodec libx264 -b:v 300k -r 30 -g 30 output/vid838.mp4

'''

class AV_Recorder():

	def __init__(self):
		
		self.video_device = 0
		self.num_audio_channels = 1

		self.cmd = 'ffmpeg'
		#record audio using alsa, use the default recording device
		self.rec_audio_cmd = ' -f alsa -i default'
		
		self.rec_video_v4l2 = ' -f v4l2 -i /dev/video%d' % self.video_device
		#audio codec for v4l2 (codec is aac, bitrate is 64k)
		self.rec_video_acodec = ' -acodec aac -strict -2 -ac %d -b:a 64k' % self.num_audio_channels
		#video codec for v4l2
		self.rec_video_vcodec = ' -vcodec libx264 -b:v 300k -r 30 -g 30'
		#record video command
		if RECORD_VIDEO_ONLY:
			self.rec_video_cmd = self.rec_video_v4l2 + self.rec_video_vcodec
		else:
			self.rec_video_cmd = self.rec_video_v4l2 + self.rec_video_acodec + self.rec_video_vcodec
		#output filename
		self.output_name = 'temp_output'
		#Popen object will be stored in pff
		self.pff = 0
		

	def generate_cmd(self):
		#final recording command for video and audio recording with ffmpeg
		if RECORD_VIDEO_ONLY:
			self.cmd = 'ffmpeg -y' + self.rec_video_cmd + ' ' + self.output_name + '.mp4'
		else:
			self.cmd = 'ffmpeg -y' + self.rec_audio_cmd + self.rec_video_cmd + ' ' + self.output_name + '.mp4'

	def record(self,filename):
		self.output_name = filename
		self.generate_cmd()
		print('\n--ffmpeg command--\n',self.cmd,'\n')
		self.pff = Popen(shlex.split(self.cmd), stdin = DEVNULL, stdout = DEVNULL, stderr = STDOUT)
		print('recording started...')

	def stop(self):
		self.pff.terminate()
		print('recording stopped.')

