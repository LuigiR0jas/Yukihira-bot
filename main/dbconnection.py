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

def getUserState(id):
    connect()
    cursor = conn.cursor()
    query0 = "SELECT state FROM users WHERE user_id = %s"
    data0 = [id]
    cursor.execute(query0, data0)
    conn.commit()
    records = cursor.fetchall() ## es un 'arreglo'
    if (len(records) == 0):
        return 'null'
    else:
        return records[0]

def saveUserState(id, state):
    connect()
    cursor = conn.cursor()
    query0 = "UPDATE users SET state= %s WHERE user_id = %s"
    data0 = (state,id)
    cursor.execute(query0, data0)
    conn.commit()

def getUserRestaurant(id):
    connect()
    cursor = conn.cursor()
    query = "SELECT * FROM restaurant WHERE owner_id = %s"
    data = [id]
    cursor.execute(query, data)
    conn.commit()
    restaurants = cursor.fetchall()
    if (len(restaurants) == 0):
        return 'null'
    else:
        print(restaurants)
        return restaurants[0]
