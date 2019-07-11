import os

'''
run this script to reset the device, that is remove all the entries from the local database, and delete all saved question and answer videos
'''

os.system("rm -f *.npz")
os.system("rm -f *.sqlite3")
os.system("cd output && rm *")
os.sytem("cd answers && rm *")
