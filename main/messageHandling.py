#------------------------------------------------------Message Handling-------------------------------------------------
import sys
import time
import telepot
import config
import dbconnection
import random
import commands
theBot = False

#Function to handle the bot object from main.py
def botHolder(bot):
    global theBot
    theBot = bot

def handle(msg):
    text = msg['text']
    chat = msg['chat']
    frome = msg['from']
    firstname = frome['first_name']
    id = frome['id']
    type = chat['type']
    date = str(msg['date'])
    if ('username' in frome):
        username = '@' + frome['username']
    else:
        username = 'N/A'
    print('·' + firstname + ' (from ' + type + ' chat), at time ' + date + ', says:\n' + text + '\n')
    analisys = analize(msg, text, id, type)

    if (isinstance(analisys, str)):
        state = dbconnection.getUserState(id)
        commands.identifyCommand(analisys, state, id, username, firstname, type, text)
    elif(analisys == 1):
        state = dbconnection.getUserState(id)
        command = commands.identifyCommandByState(state)
        # print('Again in message handler: ' + command)
        commands.identifyCommand(command, state, id, username, firstname, type, text)
    elif(analisys == 0):
        state = dbconnection.getUserState(id)
        theBot.sendMessage(id, 'I can only understand you via commands. If you need help, send /help. It was nothing!')
        # print('type is ' + type + ' and state is ' + str(state[0]) + '. Analisys is: ' )
        # print(analisys)


def analize(msg, text, id, type):
    state = dbconnection.getUserState(id)
    if('entities' in msg and state == 'null'):
        return '/start'
    elif('entities' in msg and state == 0):
        textArray = text.split(" ")
        command = textArray[0]
        print('It\'s a command, and it says: ' + command + '\n')
        return command
    elif('entities' in msg and state != 0 and type != 'group'):
        textArray = text.split(" ")
        command = textArray[0]
        if (command == "/cancel"):
            print('It\'s a cancel command')
            return command
        else:
            return 1
    else:
        if(type != 'group' and state != 0):
            print(1)
            return 1
        elif(type != 'group' and state == 0):
            print(0)
            return 0

def sendMessage(id, text):
    theBot.sendMessage(id, text)

def sendKeyboard(id, text, keyboard):
    theBot.sendMessage(id, text, reply_markup=keyboard)
