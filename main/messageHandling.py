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
    analize(msg, text, id, username, firstname)


def analize(msg, text, id, username, firstname):
    if('entities' in msg):
        textArray = text.split(" ")
        command = textArray[0]
        print('It\'s a command, and it says: ' + command + '\n')
        commands.identifyCommand(command, id, username, firstname)
    else:
        theBot.sendMessage(id, 'I can only understand you via commands. If you need help, send /help. It was nothing!')

def sendMessage(id, text):
    theBot.sendMessage(id, text)
