import sys
import time
import telepot

TOKEN = '255968429:AAGx_fxqdTManh9q8M_0zmMBPx4ZSKrA_fk';

def handle(msg):
    text = msg['text']
    chat = msg['chat']
    frome = msg['from']
    firstname = frome['first_name']
    type = chat['type']
    date = str(msg['date'])
    print('·' + firstname + ' (from ' + type + ' chat), at time ' + date + ', says:\n' + text)
    print(msg)
'''
if msg['entities'] && text == "/echo":
bot.sendMessage(text)
'''


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

#This is to keep the program running.
while 1:
    time.sleep(10)
'''
#Mensaje privado comando de bot:
{'text': '/main',
 'entities': [{'offset': 0,
              'type': 'bot_command',
               'length': 5}],
 'from': {'id': 293927703,
         'last_name': 'Panunzio',
         'first_name': 'Victor'},
 'date': 1475716876,
 'message_id': 38,
 'chat': {'id': 293927703,
         'last_name': 'Panunzio',
         'first_name': 'Victor',
         'type': 'private'}}

#Mensaje privado texto plano:
{'date': 1475716878,
 'text': 'lel',
 'message_id': 39,
 'chat': {'username': 'YiyiRojas',
          'id': 128888164,
          'first_name': 'Luigi',
          'type': 'private'},
 'from': {'username': 'YiyiRojas',
         'id': 128888164,
         'first_name': 'Luigi'}}

#Mensaje grupo texto plano:
{'date': 1475769348,
 'chat': {'all_members_are_administrators': False,
          'type': 'group',
          'title': 'AI Testing Lab.',
          'id': -164799258},
 'text': 'testing',
 'from': {'first_name': 'Luigi',
           'username': 'YiyiRojas',
           'id': 128888164},
           'message_id': 88}

#Mensaje grupo comando de bot:
{'message_id': 93,
 'date': 1475769683,
 'from': {'last_name': 'Panunzio',
          'id': 293927703,
          'first_name': 'Victor'},
 'chat': {'type': 'group',
          'id': -164799258,
          'title': 'AI Testing Lab.',
          'all_members_are_administrators': False},
'entities': [{'offset': 0,
            'type': 'bot_command',
            'length': 5}],
'text': '/help'}

{'chat': {'first_name': 'Victor',
          'id': 293927703,
          'type': 'private',
          'last_name': 'Panunzio'},
 'text': '/echo hola',
 'date': 1475770715,
 'from': {'first_name': 'Victor',
          'id': 293927703,
          'last_name': 'Panunzio'},
 'message_id': 100,
 'entities': [{'length': 5,
               'type': 'bot_command',
               'offset': 0}]
}

          '''
