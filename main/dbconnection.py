#--------------------------------------------------------Database Connection-----------------------------------------------------
import psycopg2
import config
conn = False

def connect():
    try:
        global conn
        conn = psycopg2.connect("dbname='yukihirabot_db' user='luigi' host='localhost' password=" + config.DBPass)
        # print('Connected to database')
    except Exception as e:
        print('I am unable to connect the database. Error: ' + e)
