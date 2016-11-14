#@YukihiraBot v0.0.4
import sys
import time
import telepot
import psycopg2
import config #where passwords and keys are securely stored
import dbconnection
import messageHandling

TOKEN = config.apiKey

bot = telepot.Bot(TOKEN)
bot.message_loop(messageHandling.handle)
messageHandling.botHolder(bot)
print ('*beep* *blop* YukihiraBot v0.0.4 started, listening to new messages ...')

#This is to keep the program running.
while 1:
    time.sleep(10)
