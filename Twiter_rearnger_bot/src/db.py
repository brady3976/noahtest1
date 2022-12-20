import sqlite3
import pandas as pd




# cursor.execute('''
#           CREATE TABLE IF NOT EXISTS users
#           ([screen_name] TEXT PRIMARY KEY, [last_posted] TEXT)
#           ''')

def insert(screen_name , post_info):
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    cursor.execute('''
        INSERT INTO users (screen_name, last_posted)

                VALUES
                (\''''+screen_name+'''\',\''''+post_info+'''\')
        ''')
    con.commit()
    cursor.close()
    return True
def updateExisting(screen_name , post_info):
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    updater = """Update users set last_posted = ? where screen_name = ?"""
    data= (post_info,screen_name)
    cursor.execute(updater,data)
    con.commit()
    cursor.close()
    return True
def get_screen_list():
    con = sqlite3.connect('db.sqlite')
    cursor = con.cursor()
    screen_names = list()
    cursor.execute('''
          SELECT
          a.screen_name,
          a.last_posted
          FROM users a
          
          ''')
    data = pd.DataFrame(cursor.fetchall(),columns=['screen_name','last_posted'])
    cursor.close()
    return data