import sys
import time
import telepot
import config
import dbconnection
import random
import messageHandling

def identifyCommand(command, id, username, firstname):
    if (command == '/start'):
        messageHandling.sendMessage(id, "I'm currently under development, please be patient! Although I'm adding you to my database ;)")
        clientID = 0
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "SELECT user_id FROM users WHERE user_id = %s"
        data0 = [id]
        cursor.execute(query0, data0)
        conn.commit()
        records = cursor.fetchall()
        if (len(records) == 0):
            idExists = True
            while (idExists):
                clientID += 1
                query1 = "SELECT client_id FROM client WHERE client_id = %s"
                data1 = [clientID]
                cursor.execute(query1, data1)
                conn.commit()
                records1 = cursor.fetchall()
                if (len(records1) == 0):
                    idExists = False
            query2 = "INSERT INTO users (user_id, user_name, user_firstname) VALUES (%s, %s, %s)"
            query3 = "INSERT INTO client (user_id, client_id) VALUES (%s, %s)"
            data2 = (id, username, firstname)
            data3 = (id, clientID)
            cursor.execute(query2, data2)
            cursor.execute(query3, data3)
            conn.commit()
            print('User ' + firstname + '(ID: ' + str(id) + ', username: ' + username + ')' + ' is new, therefore has been added to the database')

    elif (command == '/help'):
        messageHandling.sendMessage(id, '/help: shows this message \nMore comming soon!')

    else:
        messageHandling.sendMessage(id, "If you need help, send /help")
