import sys
import time
import telepot
import config
import dbconnection
import random
import messageHandling

TOKEN = config.apiKey
restaurantName = "null"
restaurantCategory = "null"
restaurantDescription = "null"
restaurantAddress = "null"
userID = "null"

# def addOrDelete(responds):
#     if(responds == "add"):
#         messageHandling.sendMessage(id,"Write the new dish's name")
#         dishName = text
#         executeQuery("INSERT INTO dishes (user_id, user_name, user_firstname)", [text], False)
#         return responds = "If you want to add or delete other dish use again 'add' or 'delete'"
#     elif(responds == "delete"):
#         messageHandling.sendMessage(id,"what dish do you want to delete?")
#         executeQuery("DELETE ", [text], False)
#         return responds = "If you want to add or delete other dish use again 'add' or 'delete'"

def restaurantList(listR):
    arr = []
    for list in listR:
        for x in list:
            arr.append(x)
    return arr

def identifyCommandByState(state):
    if (state >= 10 and state < 20):
        print('Identifying command, state is ' + str(state))
        return "/newrestaurant"
    elif (state >= 20 and state < 30):
        print('Identifying command, state is ' + str(state))
        return "/changechef"
    elif (state >= 30 and state < 40):
        print('Identifying command, state is ' + str(state))
        return "/restdescription"
    elif (state >= 40 and state < 50):
        print('Identifying command, state is ' + str(state))
        return "/editmenu"
    elif (state >= 50 and state < 60):
        print('Identifying command, state is ' + str(state))
        return "/editrecipe"
    elif (state >= 60 and state < 70):
        print('Identifying command, state is ' + str(state))
        return "/dishdescription"
    elif (state >= 70 and state < 80):
        print('Identifying command, state is ' + str(state))
        return "/neworder"
    elif (state >= 80 and state < 90):
        print('Identifying command, state is ' + str(state))
        return "/RestAddress"
    elif (state >= 90 and state < 100):
        print('Identifying command, state is ' + str(state))
        return "/recommendation"


def identifyCommand(command, state, id, username, firstname, type, text):
    if (command == '/start'):
        start(id, username, firstname)

    elif (command == '/help'):
        help(id)

    elif (command == '/newrestaurant'):
        NewRestaurant(state, id, username, firstname, type, text)

    elif (command == '/changechef'):
        ChangeChef(state, id, username, firstname, type, text)

    elif (command == '/restdescription'):
        RestDescription(state, id, username, firstname, type, text)

    elif (command == '/restaddress'):
        RestAddress(state, id, username, firstname, type, text)

    elif (command == '/editmenu'):
        EditMenu(state, id, username, firstname, type, text)

    elif (command == '/editrecipe'):
        EditRecipe(state, id, username, firstname, type, text)

    elif (command == '/dishdescription'):
        DishDescription(state, id, username, firstname, type, text)

    elif (command == '/neworder'):
        NewOrder(state, id, username, firstname, type, text)

    elif (command == '/recommendation'):
        recommendation(state, id, username, firstname, text)
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
    messageHandling.sendMessage(id, 'Command list:\n /newrestaurant --- Creates a new Restaurant \n/changechef --- Manage the chef of your restaurant \n/restdescription --- Set a description for your restaurant \n/editmenu --- Create or update your restaurant’s menu \n/editrecipe --- Creates or edit a recipe for your menu \n/dishdescription --- Set a description for your dish \n /neworder --- Order the dish you want from any of the available restaurants')

def NewRestaurant(state, id, username, firstname, type, text):
    if (state == 0):
        messageHandling.sendMessage(id, "What’s the name of your restaurant?")
        dbconnection.saveUserState(id, 11) # guarda el estado en la base de datos para saber en que comando y altura esta
    if (state == 11):
        global restaurantName
        restaurantName = text
        dbrestaurantName = dbconnection.executeQuery("SELECT * FROM restaurant WHERE restaurant_name = %s", [restaurantName], True)
        if (dbrestaurantName == 'null'):
            keyboard = [["Seafood", "Steakhouse", "Fastfood"], ["Vegetarian", "International", "Other"]]
            ReplyKeyboardMarkup = { "keyboard": keyboard, "one_time_keyboard" : True }
            messageHandling.sendKeyboard(id, "Ok, type the restaurant's specialty", ReplyKeyboardMarkup);
            dbconnection.saveUserState(id, 12)
        else:
            messageHandling.sendMessage(id, "There's already another restaurant with that name")
    if (state == 12):
        global restaurantCategory
        restaurantCategory = text
        ownerID = dbconnection.executeQuery("SELECT owner_id FROM owner WHERE user_id=%s", [id], True)
        chefID = dbconnection.executeQuery("SELECT chef_id FROM chef WHERE user_id=%s", [id], True)
        if (ownerID == 'null'):
            dbconnection.executeQuery("INSERT INTO owner (user_id) VALUES (%s)", [id], False)
            ownerID = dbconnection.executeQuery("SELECT owner_id FROM owner WHERE user_id=%s", [id], True)
        if (chefID == 'null'):
            dbconnection.executeQuery("INSERT INTO chef (user_id) VALUES (%s)", [id], False)
            chefID = dbconnection.executeQuery("SELECT chef_id FROM chef WHERE user_id=%s", [id], True)

        dbconnection.executeQuery("INSERT INTO restaurant (chef_id, user_id, owner_id, restaurant_name, restaurant_category) VALUES (%s, %s, %s, %s, %s)", (chefID[0], id, ownerID[0], restaurantName, restaurantCategory), False)
        messageHandling.sendMessage(id, 'Congratulations ' + username + ', you are the new owner and main chef of ' + restaurantName + '. If you want to create the menu for your restaurant, use the /editmenu command, and if you are not the Chef of the restaurant type /changechef to assign a new one')
        dbconnection.saveUserState(id, 0)

# def ChangeChef(state, id, username, firstname, type, text):
#     if (state == 0):
#         restaurants = dbconnection.executeQuery("SELECT restaurant_name FROM restaurant WHERE user_id = %s", [id], True)
#         if(restaurants == "null"):
#             messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the command /newrestaurant")
#             dbconnection.saveUserState(id,0)
#         else:
#             arr = restaurantList(restaurants)
#             messageHandling.sendKeyboard(id, "Select the restaurant which chef you want to change", {"keyboard": [arr], "one_time_keyboard":True})
#             dbconnection.saveUserState(id,21)
#     if (state == 21):
#         global restaurantName
#         restaurantName = text
#         chefQuery =  dbconnection.executeQuery("SELECT chef_id FROM restaurant WHERE restaurant_name= %s", [restaurantName], True)
#         chef = restaurantList(chefQuery)
#         chefUserID = dbconnection.executeQuery("SELECT user_id FROM chef WHERE chef_id=%s", [chef[0]], True)
#         global userID
#         userID = restaurantList(chefUserID)
#         user = dbconnection.executeQuery("SELECT user_name, user_firstname FROM users WHERE user_id=%s", [userID[0]], True)
#         userData = restaurantList(user)
#         if (userData[0] != 'N/A'):
#             chefName = userData[0]
#         else:
#             chefName = userData[1]
#         messageHandling.sendMessage(id, "The current chef of restaurant "+ restaurantName +" is "+ chefName +", write the username of the new chef. (Please note that, prior to send the username of the chef, he must have a username and have started a conversation with me).")
#         dbconnection.saveUserState(id, 22)
#     if (state == 22):
#         username = text
#         isChef = dbconnection.executeQuery("SELECT user_id, user_firstname FROM users WHERE user_name= %s", [text], True)
#         newChef = restaurantList(isChef)
#         if (isChef == 'null'):
#             messageHandling.sendMessage(id, "That user is not registered. Please verify that the provided username is correct or that your chef has talked to me prior to doing this process.")
#         else:
#             print(newChef[0])
#             dbconnection.executeQuery("UPDATE restaurant SET user_id= %s WHERE user_id= %s", [newChef[0], userID[0]], False )
#             dbconnection.executeQuery("UPDATE chef SET user_id= %s WHERE user_id= %s", [newChef[0], userID[0]], False)
#             if (newChef[1] == 'N/A'):
#                 chefName = newChef[1]
#             else:
#                 chefName = text
#             messageHandling.sendMessage(id, "Chef changed, the new chef is now " + chefName)
#             dbconnection.saveUserState(id, 0)

def RestDescription(state, id, username, firstname, type, text):
    if (state == 0):
        restaurants = dbconnection.executeQuery("SELECT restaurant_name FROM restaurant WHERE user_id = %s", [id], True)
        if (restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /newrestaurant")
            dbconnection.saveUserState(id,0)
        else:
            arr = restaurantList(restaurants)
            messageHandling.sendKeyboard(id, "Select the restaurant to add a description ", {"keyboard": [arr], "one_time_keyboard":True})
            dbconnection.saveUserState(id,31)
    if (state == 31):
        global restaurantName
        restaurantName = text
        messageHandling.sendMessage(id, "Type your restaurant description to " + restaurantName + " (max 400 characters)")
        dbconnection.saveUserState(id,32)
    if (state == 32):
        global restaurantDescription
        restaurantDescription = text
        dbconnection.executeQuery("UPDATE restaurant SET restaurant_description= %s WHERE restaurant_name = %s", [restaurantDescription, restaurantName], False)
        messageHandling.sendMessage(id, "The description of " + restaurantName + " has been changed")
        dbconnection.saveUserState(id, 0)

def RestAddress(state, id, username, firstname, type, text):
    if (state == 0):
        restaurants = dbconnection.executeQuery("SELECT restaurant_name FROM restaurant WHERE user_id = %s", [id], True)
        if (restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
            dbconnection.saveUserState(id,0)
        else:
            arr = restaurantList(restaurants)
            messageHandling.sendKeyboard(id, "Select the restaurant to add an address ", {"keyboard": [arr], "one_time_keyboard":True})
            dbconnection.saveUserState(id,81)
    if (state == 81):
        global restaurantName
        restaurantName = text
        messageHandling.sendMessage(id, "Type your restaurant address to " + restaurantName )
        dbconnection.saveUserState(id,82)
    if (state == 82):
        global restaurantAddress
        restaurantAddress = text
        dbconnection.executeQuery("UPDATE restaurant SET restaurant_description= %s WHERE restaurant_name = %s", [restaurantAddress, restaurantName], False)
        messageHandling.sendMessage(id, "The description of " + restaurantName + " has been changed")
        dbconnection.saveUserState(id, 0)

def EditMenu(state, id, username, firstname, type):
    print("algo")
    # if (state == 0):
    #     restaurants = executeQuery("SELECT restaurant_name FROM restaurant WHERE owner_id = %s", [id], True)
    #     if(restaurants == "null"):
    #         messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
    #         dbconnection.saveUserState(id,0)
    #     else:
    #         arr = restaurantList(restaurants)
    #         messageHandling.sendKeyboard(id, "Select the restaurant to add a Menu", {"keyboard": [[arr]], "one_time_keyboard":True})
    #         dbconnection.saveUserState(id,41)
    #         if (state == 41):
    #             global restaurantName
    #             restaurant = text               #revisar
    #             dishes = executeQuery("SELECT *from dishes where restaurant_id= %s", [restaurants], True)
    #             if(dishes == "null"):
    #                 messageHandling.sendMessage(id, "The restaurant "+ restaurantName+ "dosen't have a Menu, to create it send 'add'")
    #                 dbconnection.saveUserState(id, 42)
    #                 if(state == 42):
    #                     while(text == "add" || text == "delete"):
    #                         x = addOrDelete(text)
    #                         messageHandling(x)
                #
                #
                #
                #
                # else:
                #     messageHandling.sendMessage(id, "If you want to add or delete a dishes use 'add' or 'delete'")
                #     if
                #
                #
                # messageHandling.sendMessage(id, "Type your restaurant description (max 400 characters)")
                # dbconnection.saveUserState(id,42)

def EditMenu(state, id, username, firstname, type, text):
    if (state == 0):
        restaurants = dbconnection.executeQuery("SELECT restaurant_name FROM restaurant WHERE user_id = %s", [id], True)
        if(restaurants == "null"):
            messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
            dbconnection.saveUserState(id,0)
        else:
            arr = objectList(restaurants)
            messageHandling.sendKeyboard(id, "Select the restaurant to add a Menu", {"keyboard": [arr], "one_time_keyboard":True})
            dbconnection.saveUserState(id,41)
    if (state == 41):
            global restaurantName
            restaurantName = text
            restID = dbconnection.executeQuery("SELECT restaurant_id FROM restaurant WHERE restaurant_name= %s", [restaurantName], True)             #revisar
            print(restID)
            dishes = dbconnection.executeQuery("SELECT dish_name FROM dishes WHERE restaurant_id= %s", [restID[0]], True)
            if(dishes == "null"):
                messageHandling.sendKeyboard(id, "The restaurant "+ restaurantName + " dosen't have a Menu, to create it send 'add'", {"keyboard": [["Add"], ["Cancel"]], "one_time_keyboard":True})
                dbconnection.saveUserState(id, 42)
            else:
                messageHandling.sendKeyboard(id, "If you want to add or delete a dishes use 'add' or 'delete'", {"keyboard": [["Add", "Delete"], ["Cancel"]], "one_time_keyboard":True})
                dbconnection.saveUserState(id, 42)
    if(state == 42):
        if(text == "Add"):
            messageHandling.sendMessage(id,"Write the new dish's name")
            dbconnection.saveUserState(id, 43)
        elif(text == "Delete"):
            messageHandling.sendMessage(id,"what dish do you want to delete?") #crear un customkye
            dbconnection.saveUserState(id, 46)
        elif(text == "Cancel"):
            messageHandling.sendMessage(id, "Comand has been canceled")
            dbconnection.saveUserState(id, 0)
    if(state == 43):
        global dishName
        dishName = text
        messageHandling.sendMessage(id, "Price of the dish")
        dbconnection.saveUserState(id, 44)
    if(state == 44):
        global dishPrice
        dishPrice = text
        messageHandling.sendMessage(id, "Type the description to "+ dishName)
        dbconnection.saveUserState(id, 45)
    if(state == 45):
        dishDescription = text
        data = dbconnection.executeQuery("SELECT chef_id, owner_id, restaurant_id, restaurant_category FROM restaurant WHERE restaurant_name= %s AND user_id= %s", [ restaurantName, id], True)
        arr = objectList(data)
        dbconnection.executeQuery("INSERT INTO dishes (chef_id, owner_id, restaurant_id, dish_name, dish_category, dish_price, dish_description, dish_demand ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", [arr[0], arr[1], arr[2], dishName,  arr[3], dishPrice, dishDescription, "1"], False)
        dbconnection.saveUserState(id, 47)
    if(state == 46):
        dishName = text
        dbconnection.executeQuery("DELETE FROM dishes WHERE dish_name=%s AND restaurant_id= %s ", [dishName, restID[0]], False)
        dbconnection.saveUserState(id, 47)
    if(state == 47):
        messageHandling.sendKeyboard(id, "If you want to add or delete another dish use 'add' or 'delete'", {"keyboard": [["Add", "Delete"], ["Cancel"]], "one_time_keyboard":True})
        if(text == "Add" or text == "Delete"):
            dbconnection.saveUserState(id, 42)
        else:
            dbconnection.saveUserState(id, 0)








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
    print("algo")
    #  if (state == 0):
    #      restaurants = executeQuery("SELECT restaurant_name FROM restaurant WHERE owner_id = %s", [id], True)
    #      if(restaurants == "null"):
    #          messageHandling.sendMessage(id, "You don't have any restaurant. To create one use the comand /NewRestaurant")
    #          dbconnection.saveUserState(id,0)
    #      else:
    #          messageHandling.sendMessage(id, "Select the restaurant of the dish which description you want to change/create" + restaurants)
    #          dbconnection.saveUserState(id,61)
    #          if (state == 61):
    #              global restaurantName
    #              restaurantName = text               #revisar
    #              dishes = executeQuery("SELECT dish_name from dishes where restaurant_name= %s", [restaurantName], True)
    #              if(dishes == "null"):
    #                  messageHandling.sendMessage(id, "The restaurant "+ restaurantName + "doesn't have a Menu, to create it use the comand /EditMenu")
    #                  dbconnection.saveUserState(id, 62)
    #              else:
    #                  messageHandling.sendMessage(id, "Choose the dish to add a description")
    #                  dishName = text
    #                  dishName2 = executeQuery("SELECT dish_name FROM dishes where dish_name= %s AND owner_id= %s", [dishName, id],True)
    #                  if(dishName2 == null):
    #                      messageHandling.sendMessage(id, "There are no dish with that name")
    #                  else:
    #                      messageHandling.sendMessage(id, "Type the description of " + dishName2 + "(Max characters 400)")
    #                      dishDescription = text
    #                      executeQuery("UPDATE dishes SET dish_description= %s WHERE dish_name= %s & user_id= %s ", [dishDescription, dishName2, id],False)


def NewOrder(state, id, username, firstname, type, text):
    if (state == 0):
        messageHandling.sendMessage(id, "You're inside NewOrder function, on state 70, please send me another message to get out of here")
        dbconnection.saveUserState(id, 71)
    if (state == 71):
        messageHandling.sendMessage(id, "You're inside NewOrder function, on state 71. Another one and you'll be free!")
        dbconnection.saveUserState(id, 72)
    if (state == 72):
        messageHandling.sendMessage(id, "hahaha you're now trapped in NewOrder function, on state 72! No matter what you do, you can't leave this place")

def recommendation(state, id, username, firstname, text):
    if (state == 0):
        isChef = dbconnection.executeQuery('SELECT * FROM chef WHERE user_id=%s', [id], True)
        if (isChef != 'null'):
            messageHandling.sendMessage(id, "You're not a chef, if you wanna join the club, create a new restaurant! use /newrestaurant")
        else:
            chef = restaurantList(isChef)

def cancel(id):
    dbconnection.saveUserState(id, 0)
    messageHandling.sendMessage(id, "Oww :C. You found my weakness! Very well, your state is now 0 again")
