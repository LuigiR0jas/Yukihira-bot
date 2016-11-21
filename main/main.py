#@YukihiraBot v0.0.5
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
print ('*beep* *blop* YukihiraBot v0.0.5 started, listening to new messages ...')

#This is to keep the program running.
while 1:
    time.sleep(10)
