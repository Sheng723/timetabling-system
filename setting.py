import os
import sqlite3

# create and initialize global variable
def init():
    global dbname
    dbname = ""
    
# if the database available in the file, return true, else return false
def isSqlite3Db(db):
    if os.path.isfile(db):
        if os.path.getsize(db) > 100:
            with open(db,'r', encoding = "ISO-8859-1") as f:
                header = f.read(100)
                if header.startswith('SQLite format 3'):
                    return True