#@YukihiraBot v0.0.3
import sys
import time
import telepot
import psycopg2

TOKEN = '*******************************************';

#--------------------------------------------------------Database Connection----------------------------------------------------------
try:
    conn = psycopg2.connect("dbname='bot_test' user='luigi' host='localhost' password='****'")
    print('Connected\n')
except Exception as e:
    print('I am unable to connect the database. Error: ' + e + '\n')

cur = conn.cursor()
cur.execute("""SELECT datname from pg_database""")
rows = cur.fetchall()
for row in rows:
    print("    ", row[0])

#------------------------------------------------------Message Handling----------------------------------------------------------------------
def handle(msg):
    text = msg['text']
    chat = msg['chat']
    frome = msg['from']
    firstname = frome['first_name']
    type = chat['type']
    date = str(msg['date'])
    print('·' + firstname + ' (from ' + type + ' chat), at time ' + date + ', says:\n' + text + '\n')
    #print(msg)
    analize(msg)

def analize(msg):
        if('entities' in msg):
            analizedText = msg['text']
            textArray = analizedText.split(" ")
            command = textArray[0]
            print('It\'s a command, and it says: ' + command + '\n')

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

#This is to keep the program running.
while 1:
    time.sleep(10)
