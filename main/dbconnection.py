#--------------------------------------------------------Database Connection-----------------------------------------------------
import psycopg2
import config
conn = False

def connect():
    try:
        global conn
        conn = psycopg2.connect("dbname='yukihira_bot' user='luigi' host='localhost' password=" + config.DBPass)
        # print('Connected to database')
    except Exception as e:
        print('I am unable to connect the database. Error: ' + str(e))

def executeQuery(query, data, bool):
    connect()
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    if bool:
        records = cursor.fetchall()
        if (len(records) == 0):
            return 'null'
        else:
            return records

def getUserState(id):
    query = "SELECT state FROM users WHERE user_id = %s"
    data = [id]
    executeQuery(query, data, True)


def saveUserState(id, state):
    query = "UPDATE users SET state= %s WHERE user_id = %s"
    data = (state,id)
    executeQuery(query, data, False)
