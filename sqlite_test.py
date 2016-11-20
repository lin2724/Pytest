import sqlite3
import os
import datetime
import time

db_path = os.path.join('other', 'test.db')
print db_path


if not os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    con.execute('CREATE TABLE url_record(\
      url CHAR PRIMARY KEY ,\
      count INT DEFAULT 0,\
      desciption CHAR ,\
      is_done INT DEFAULT 0,\
      record_time DATE )')
    con.commit()
else:
    con = sqlite3.connect(db_path)
    now = datetime.datetime.now()
    print now
    con.execute('INSERT INTO url_record VALUES (?,?,?,?,?)', ('httpxx', 1, 'hello',1 ,now))
    con.commit()
con.close()

