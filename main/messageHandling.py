#------------------------------------------------------Message Handling-------------------------------------------------
import sys
import time
import main
import telepot
import config #where passwords and keys are securely stored
import dbconnection
import random
import commands

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
        username = 'Not Specified'
    print('·' + firstname + ' (from ' + type + ' chat), at time ' + date + ', says:\n' + text + '\n')
    # isNew(id, username, firstname)
    analize(msg, text, id)


def analize(msg, text, id):
    if('entities' in msg):
        textArray = text.split(" ")
        command = textArray[0]
        print('It\'s a command, and it says: ' + command + '\n')
        commands.identifyCommand(command, id)
