import json
from datetime import datetime
from config import *
import sqlite3 as sql


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
https://stackabuse.com/a-sqlite-tutorial-with-python/

'''

#to connect to the sqlite3 database

#global connection variable to the database
con = None

def db_connect(db_path = DB_PATH):
	global con
	if con:
		return con
	else:
		try:
			con = sql.connect(db_path)
		except:
			print('Unable to connect to the database! Please verify the DB_PATH in config.py')
			return None
		return con


def create_tables():
	con = db_connect()
	if con:
		cur = con.cursor()
		json_sent_table = """
			CREATE TABLE json_sent (
			lid text PRIMARY KEY,
			id text
			)
			"""
		try:
			cur.execute(json_sent_table)
			print('json_sent table created successfully')
		except:
			print('Unable to create table!')
		video_sent_table = """
			CREATE TABLE video_sent (
				lid text PRIMARY KEY,
				id text
				)
			"""
		try:
			cur.execute(video_sent_table)
			print('video_sent table created successfully')
		except:
			print('Unable to create table!')
		return con
	else:
		return None


def check_tables():
	con = db_connect()
	if con:
		cur = con.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
		list_db = cur.fetchall() 
		for i in range(len(list_db)):
			list_db[i] = list_db[i][0]
		if 'json_sent' in list_db and 'video_sent' in list_db:
			return True
		else:
			return False
	else:
		return False


json_sent_sql = "INSERT INTO json_sent (lid,id) VALUES (?,?)"
vid_sent_sql = "INSERT INTO video_sent (lid,id) VALUES (?,?)"
del_from_json_sent = "DELETE FROM json_sent where lid = ?"

def check_json_post_status(vidname):
	local_id = vidname.split('.')[0]
	con = db_connect()
	if con and check_tables():
		cur = con.cursor()
		cur.execute("SELECT lid,id FROM json_sent")
		results = cur.fetchall()
		for lid,id in results:
			if lid == local_id:
				return id
		return False
	else:
		return False

def json_post_success(vidname,id):
	local_id = vidname.split('.')[0]
	con = db_connect()
	if con:
		if not check_tables():
			create_tables()
		cur = con.cursor()
		try:
			cur.execute(json_sent_sql,(local_id,id))
			con.commit()
			return True
		except:
			con.rollback()
			print("[ERROR]: Cannot add entry to json_sent table!")
	return False

def video_post_success(vidname,id):
	local_id = vidname.split('.')[0]
	con = db_connect()
	if con:
		if not check_tables():
			create_tables()
		cur = con.cursor()
		try:
			cur.execute(vid_sent_sql,(local_id,id))
			cur.execute(del_from_json_sent,(local_id,))
			con.commit()
			return True
		except:
			con.rollback()
			print("[ERROR]: Cannot add entry to video_sent table!")
	return False	

def get_posted_qids():
	con = db_connect()
	if con and check_tables():
		cur = con.cursor()
		try:
			cur.execute("SELECT id from video_sent")
			results = cur.fetchall()
			for i in range(len(results)):
				results[i] = results[i][0]
			return results
		except:
			print('[ERROR]: Problems fetching ids from video_sent table!')
	return []

def get_remote2local_dict():
	con = db_connect()
	if con and check_tables():
		cur = con.cursor()
		r2l = {}
		try:
			cur.execute("SELECT lid,id from video_sent")
			results = cur.fetchall()
			for r in results:
				r2l[r[1]] = r[0]
		except: 
			print('[ERROR]: Problems fetching ids from video_sent table!')
	return r2l

def new_log_entry(filename,ext ='mp4'):
	now = datetime.now()
	ldb = {}
	ldb['name'] = filename
	ldb['date'] = now.strftime("%d/%m/%y")
	ldb['time'] = now.strftime("%H:%M:%S")
	ldb['machine_id'] = MACHINE_ID
	ldb['vid_ext'] = ext

	#add the json extension
	jsonfile = filename + '.json'
	vidname=filename+ '.' + ext
	with open(OUTPUT_DIR+jsonfile,'w+') as outfile:
		json.dump(ldb,outfile)	
	return



