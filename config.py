#Config file for settings

RPI = False

MACHINE_ID = 'AbC'
API_HOST = '10.196.17.146'
API_PORT = 8081
OUTPUT_DIR = 'output/'
RECORD_VIDEO_ONLY = False
if RPI:
	RPI_CMD = True
	LOW_SETTING = False
else:
	RPI_CMD = False
	LOW_SETTING = True

DB_PATH = 'database.sqlite3'
