import sys
import time
import telepot
import config
import dbconnection
import random
import messageHandling

#Manejar hilos de conversacion
#Manejar ciclos repetitivos para asegurar la integridad de los datos ingresados
#Crear funcion para manejar los queries de forma más sencilla

def identifyCommand(command, id, username, firstname, type):
    if (command == '/start'):
        messageHandling.sendMessage(id, "Welcome my name is YukihiraBot. What can I do for you? \n If you want to create a new restaurant you can do it typing the /NewRestaurant command. If you want to make an order, please type /NewOrder If you want some more information use the /help command")
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "SELECT user_id FROM users WHERE user_id = %s"
        data0 = [id]
        cursor.execute(query0, data0)
        conn.commit()
        records = cursor.fetchall()

        if (len(records) == 0):
            query2 = "INSERT INTO users (user_id, user_name, user_firstname) VALUES (%s, %s, %s)"
            query3 = "INSERT INTO client (user_id) VALUES (%s)"
            data2 = (id, username, firstname)
            data3 = [id]
            cursor.execute(query2, data2)
            cursor.execute(query3, data3)
            conn.commit()
            print('User ' + firstname + '(ID: ' + str(id) + ', username: ' + username + ')' + ' is new, therefore has been added to the database')


    elif (command == '/help'):
        messageHandling.sendMessage(id, 'Command list:\n /NewRestaurant --- Creates a new Restaurant \n/ChangeChef --- Manage the chef of your restaurant \n/RestDescription --- Set a description for your restaurant \n/EditMenu --- Create or update your restaurant’s menu \n/EditRecipe --- Creates or edit a recipe for your menu \n/DishDescription --- Set a description for your dish \n /NewOrder --- Order the dish you want from any of the available restaurants')

    elif (command == '/NewRestaurant'):
        messageHandling.sendMessage(id, "What’s the name of your restaurant?")
        #User sends the restaurant’s name
        restaurantName = msg.txt; #Whatever the user sends
        messageHandling.sendMessage(id, "Ok, type the number of the restaurant's specialty");
        messageHandling.sendMessage(id, "1. Seafood \n2.Grill/Steakhouse \n3.Fastfood \n4.Vegetarian \n5.International \n6.Italian \n7.Chinese \n8.Mexican\n9.Other");
        #User sends the restaurant’s category
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "INSERT INTO restaurant (chef_id, owner_id, restaurant_demand, restaurant_name, restaurant_description, restaurant_adress) VALUES (%s, %s, %s, %s, %s, %s)"
        data0 = (id, id, 0, restaurantName,'', '')
        cursor.execute(query0, data0)
        conn.commit()
        #Chef: user_name (default)
        messageHandling.sendMessage(id, 'Congratulations' + username + ', you are the new owner and main chef of' + restaurantName + '.If you want to create the menu for your restaurant, use the /EditMenu command, and if you are not the Chef of the restaurant type /ChangeChef to assign a new one')

    elif (command == '/ChangeChef'):
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "SELECT restaurant_name FROM restaurant WHERE owner_id = %s"
        query1 = "SELECT chef_id FROM restaurant WHERE owner_id = %s"
        data0 = [id]
        data1 = [id]
        cursor.execute(query0, data0)
        conn.commit()
        records = cursor.fetchall()
        cursor.execute(query1, data1)
        conn.commit()
        records1 = cursor.fetchall()
        restaurantName = records(0)
        currentChefID = records1(0)
        messageHandling.sendMessage(id, 'The current chef of ' + restaurantName+ ' is ' + currentChefID +', write the id of your new chef')
        #User types chef’s username
        newChefID = msg.txt
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "UPDATE restaurant (chef_id) VALUES (%s) WHERE owner_id = %s"
        data0 = (newChefID, id)
        cursor.execute(query0, data0)
        conn.commit()
        messageHandling.sendMessage(id, 'The new chef of ' + restaurantName + ' is ' + NewChefID)

    elif (command == '/RestDescription'):
        messageHandling.sendMessage(id,'Type your restaurant description (max 400 characters)')
        #User sends description
        restaurantDescription = msg.txt
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "UPDATE restaurant (restaurant_description) VALUES (%s) WHERE owner_id = %s"
        data0 = (restaurantDescription, id)
        cursor.execute(query0, data0)
        conn.commit()
        messageHandling.sendMessage(id,'“The description of (restaurant_name) has been changed”')

    elif (command == '/EditMenu'):
        messageHandling.sendMessage(id,)

    elif (command == 'EditRecipe'):
        messageHandling.sendMessage(id,)

    elif (command == '/DishDescription'):
        messageHandling.sendMessage(id,)

    elif (command == '/NewOrder'):
        messageHandling.sendMessage(id,)

    else:
        if(type != 'group'):
            messageHandling.sendMessage(id, "If you need help, send /help")
