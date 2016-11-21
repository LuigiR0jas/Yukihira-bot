import sys
import time
import telepot
import config
import dbconnection
import random
import messageHandling

#Crear funcion que determine si el usuario tiene o no tiene restaurante
#funcion para mostrar los restaurantes del usuario

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
        #User: *types the restaurant’s name *
        #investigar para la entrada por teclado
        # Bot: “Ok, choose the restaurant’s speciality” 	(KEYBOARD)
        # •	Seafood
        # •	Grilly/Stakehouse
        # •	Fast food
        # •	Vegetarian
        # •	International:
        # o	Italian
        # o	Chinese
        # o	Mexican
        # •	Other
        #User: *chooses the restaurant’s category*
        #Owner: user_name (default)
        #Chef: user_name (default)
        messageHandling.sendMessage(id, 'Congratulations (user_name), you are the new Owner and main        Chef of (restaurant_name). If you want to create the menu for your restaurant                use the /EditMenu command, and if you are not the Chef of the restaurant type                /ChangeChef to assign a new one')

    elif (command == '/ChangeChef'):
        messageHandling.sendMessage(id, 'Select the restaurant of the chef you want to change')
        #User:  *selects the restaurant*

        messageHandling.sendMessage(id, 'The current chef of (restaurant_name) is (chef_name),                                   write the username of your new chef')

        #User:  *types chef’s username*
        messageHandling.sendMessage(id, 'The new chef of (restaurant_name) is (chef_name).')

    elif (command == '/RestDescription'):
        messageHandling.sendMessage(id,'“Select the restaurant” *shows the user’s restaurant*')
        #User: *selects*
        messageHandling.sendMessage(id,'Type your restaurant description (max 400 characters)')
        #User: *types*
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
