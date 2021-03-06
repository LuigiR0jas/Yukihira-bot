import sys
import time
import telepot
import config
import dbconnection
import random
import messageHandling
from telepot.delegate import pave_event_space, per_chat_id, create_open

TOKEN = config.apiKey
restaurantName = "null"
restaurantCategory = "null"
restaurantDescription = "null"

def identifyCommandByState(state):
    if (state >= 10 and state < 20):
        print('Identifying command, state is ' + str(state))
        return "/NewRestaurant"
    elif (state >= 20 and state < 30):
        print('Identifying command, state is ' + str(state))
        return "/ChangeChef"
    elif (state >= 30 and state < 40):
        print('Identifying command, state is ' + str(state))
        return "/RestDescription"
    elif (state >= 40 and state < 50):
        print('Identifying command, state is ' + str(state))
        return "/EditMenu"
    elif (state >= 50 and state < 60):
        print('Identifying command, state is ' + str(state))
        return "/EditRecipe"
    elif (state >= 60 and state < 70):
        print('Identifying command, state is ' + str(state))
        return "/DishDescription"
    elif (state >= 70 and state < 80):
        print('Identifying command, state is ' + str(state))
        return "/NewOrder"


def identifyCommand(command, state, id, username, firstname, type, text):
    if (command == '/start'):
        start(id, username, firstname)

    elif (command == '/help'):
        help(id)

    elif (command == '/NewRestaurant'):
        NewRestaurant(state, id, username, firstname, type, text)

    elif (command == '/ChangeChef'):
        ChangeChef(state, id, username, firstname, type, text)

    elif (command == '/RestDescription'):
        RestDescription(state, id, username, firstname, type, text)

    elif (command == '/EditMenu'):
        EditMenu(state, id, username, firstname, type, text)

    elif (command == '/EditRecipe'):
        EditRecipe(state, id, username, firstname, type, text)

    elif (command == '/DishDescription'):
        DishDescription(state, id, username, firstname, type, text)

    elif (command == '/NewOrder'):
        NewOrder(state, id, username, firstname, type, text)

    elif (command == '/cancel' and state != 0):
        cancel(id)
    elif (command == '/cancel' and state == 0):
        messageHandling.sendMessage(id, "...Ok? I wasn't doing anything anyway .-.")
    else:
        if(type != 'group'):
            messageHandling.sendMessage(id, "That's not a command of mine, pal. If you need help, send /help")

def start(id, username, firstname):
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

def help(id):
    messageHandling.sendMessage(id, 'Command list:\n /NewRestaurant --- Creates a new Restaurant \n/ChangeChef --- Manage the chef of your restaurant \n/RestDescription --- Set a description for your restaurant \n/EditMenu --- Create or update your restaurant’s menu \n/EditRecipe --- Creates or edit a recipe for your menu \n/DishDescription --- Set a description for your dish \n /NewOrder --- Order the dish you want from any of the available restaurants')

def NewRestaurant(state, id, username, firstname, type, text):
    if (state == 0):
        messageHandling.sendMessage(id, "What’s the name of your restaurant?")
        dbconnection.saveUserState(id, 11) # guarda el estado en la base de datos para saber en que comando y altura esta
    if (state == 11):
        global restaurantName
        restaurantName = text #Revisar que el restaurante no esta inscrito en la db.
        messageHandling.sendMessage(id, "Ok, type the restaurant's specialty");
        dbconnection.saveUserState(id, 12) #Buscar como enviar estos datos al teclado
        messageHandling.sendMessage(id, "1. Seafood \n2.Grill/Steakhouse \n3.Fastfood \n4.Vegetarian \n5.International \n6.Italian \n7.Chinese \n8.Mexican\n9.Other");
    if (state == 12):
        global restaurantCategory
        restaurantCategory = text
        db = dbconnection.connect()
        conn = dbconnection.conn
        cursor = conn.cursor()
        query0 = "INSERT INTO chef (user_id, chef_id) VALUES (%s, %s)"
        data0 = (id, id) ##pyton es gay y prefiere string buscar diccionrio tupla lista
        query1 = "INSERT INTO owner (user_id, owner_id) VALUES (%s, %s)"
        data1 = (id, id)
        query2 = "INSERT INTO restaurant (chef_id, user_id, owner_id, restaurant_demand, restaurant_name, restaurant_description, restaurant_address, restaurant_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data2 = (id, id, id, 0, restaurantName, "", "", restaurantCategory)
        cursor.execute(query0, data0)
        cursor.execute(query1, data1)
        cursor.execute(query2, data2)
        conn.commit()
        messageHandling.sendMessage(id, 'Congratulations ' + username + ', you are the new owner and main chef of ' + restaurantName + '. If you want to create the menu for your restaurant, use the /EditMenu command, and if you are not the Chef of the restaurant type /ChangeChef to assign a new one')
        dbconnection.saveUserState(id, 0)

def ChangeChef(state, id, username, firstname, type):
    if (state == 0):
        restaurants = getUserRestaurant(id)
        if(restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
            dbconnection.saveUserState(id,0)
        else:
            messageHandling.sendMessage(id, "Select the restaurant of the chef you want to change" + restaurants)
            dbconnection.saveUserState(id,21)
            if (state == 21):
                global restaurantName
                restaurantName = text
                db = dbconnection.connect()
                conn = dbconnection.conn
                cursor = conn.cursor()
                query = ""
                messageHandling.sendMessage(id, "You're inside ChangeChef  function, on state 21. Another one and you'll be free!")
                dbconnection.saveUserState(id, 22)
            if (state == 22):
                messageHandling.sendMessage(id, "hahaha you're now trapped in ChangeChef function, on state 22! No matter what you do, you can't leave this place")


    # query0 = "SELECT restaurant_name FROM restaurant WHERE owner_id = %s"
    # query1 = "SELECT chef_id FROM restaurant WHERE owner_id = %s"
    # data0 = [id]
    # data1 = [id]
    # cursor.execute(query0, data0)
    # conn.commit()
    # records = cursor.fetchall()
    # cursor.execute(query1, data1)
    # conn.commit()
    # records1 = cursor.fetchall()
    # restaurantName = records(0)
    # currentChefID = records1(0)
    # messageHandling.sendMessage(id, 'The current chef of ' + restaurantName+ ' is ' + currentChefID +', write the id of your new chef')
    # #User types chef’s username
    # newChefID = msg.txt
    # db = dbconnection.connect()
    # conn = dbconnection.conn
    # cursor = conn.cursor()
    # query0 = "UPDATE restaurant (chef_id) VALUES (%s) WHERE owner_id = %s"
    # data0 = (newChefID, id)
    # cursor.execute(query0, data0)
    # conn.commit()
    # messageHandling.sendMessage(id, 'The new chef of ' + restaurantName + ' is ' + NewChefID)

def RestDescription(state, id, username, firstname, type, text):
    if (state == 0):
        restaurants = executeQuery("SELECT * FROM restaurant WHERE owner_id = %s", [id], True)
        if(restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
            dbconnection.saveUserState(id,0)
        else:
            messageHandling.sendMessage(id, "Select the restaurant add a description" + restaurants)
            dbconnection.saveUserState(id,31)
            if (state == 31):
                global restaurantName
                restaurant = text
                messageHandling.sendMessage(id, "Type your restaurant description (max 400 characters)")
                dbconnection.saveUserState(id,32)
            if (state == 32):
                global restaurantDescription
                restaurantDescription = text
                executeQuery("UPDATE restaurant SET restaurant_description= %s WHERE restaurant_name = %s", [restaurantDescription, restaurantName], False)
                messageHandling.sendMessage(id, "The description of" + restaurantName + "has been changed")
                dbconnection.saveUserState(id, 0)

    # query0 = "UPDATE restaurant (restaurant_description) VALUES (%s) WHERE owner_id = %s"
    # data0 = (restaurantDescription, id)
    # cursor.execute(query0, data0)
    # conn.commit()
    # messageHandling.sendMessage(id,'“The description of (restaurant_name) has been changed”')

def EditMenu(state, id, username, firstname, type):
    if (state == 0):
        restaurants = getUserRestaurant(id)
        if(restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
            dbconnection.saveUserState(id,0)
        else:
            messageHandling.sendMessage(id, "Select the restaurant to add a Menu" + restaurants)
            dbconnection.saveUserState(id,41)
            if (state == 41):
                global restaurantName
                restaurant = text
                db = dbconnection.connect()
                conn = dbconnection.conn
                cursor = conn.cursor()

                query0 = "SELECT Restaurant_ID FROM user INNER JOIN owner WHERE user.user_id = "
                data0 = (restaurantName, id)
                query1 = "SELECT FROM   WHERE restaurant_name = %s"
                data = (restaurantDescription, restaurantName)
                cursor.execute(query, data)
                conn.commit()

                messageHandling.sendMessage(id, "You're inside EditMenu function, on state 41. Another one and you'll be free!")
                dbconnection.saveUserState(id, 42)
            if (state == 42):
                messageHandling.sendMessage(id, "hahaha you're now trapped in EditMenu function, on state 42! No matter what you do, you can't leave this place")


def EditRecipe(state, id, username, firstname, type):
    if (state == 0):
        messageHandling.sendMessage(id, "You're inside EditRecipe function, on state 50, please send me another message to get out of here")
        dbconnection.saveUserState(id, 51)
    if (state == 51):
        messageHandling.sendMessage(id, "You're inside EditRecipe function, on state 51. Another one and you'll be free!")
        dbconnection.saveUserState(id, 52)
    if (state == 52):
        messageHandling.sendMessage(id, "hahaha you're now trapped in EditRecipe function, on state 52! No matter what you do, you can't leave this place")


def DishDescription(state, id, username, firstname, type):
    if (state == 0):
        messageHandling.sendMessage(id, "You're inside DishDescription function, on state 60, please send me another message to get out of here")
        dbconnection.saveUserState(id, 61)
    if (state == 61):
        messageHandling.sendMessage(id, "You're inside DishDescription function, on state 61. Another one and you'll be free!")
        dbconnection.saveUserState(id, 62)
    if (state == 62):
        messageHandling.sendMessage(id, "hahaha you're now trapped in DishDescription function, on state 62! No matter what you do, you can't leave this place")


def NewOrder(state, id, username, firstname, type):
    if (state == 0):
        messageHandling.sendMessage(id, "You're inside NewOrder function, on state 70, please send me another message to get out of here")
        dbconnection.saveUserState(id, 71)
    if (state == 71):
        messageHandling.sendMessage(id, "You're inside NewOrder function, on state 71. Another one and you'll be free!")
        dbconnection.saveUserState(id, 72)
    if (state == 72):
        messageHandling.sendMessage(id, "hahaha you're now trapped in NewOrder function, on state 72! No matter what you do, you can't leave this place")

def cancel(id):
    dbconnection.saveUserState(id, 0)
    messageHandling.sendMessage(id, "Oww :C. You found my weakness! Very well, your state is now 0 again")
