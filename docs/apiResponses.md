#-----------------------------------Dictionary API Responses examples-----------------------------------------------

#Mensaje privado comando de bot:
{'text': '/main',
 'entities': [{'offset': 0,
              'type': 'bot_command',
               'length': 5}],
 'from': {'id': 99999999,
         'last_name': 'Panunzio',
         'first_name': 'Victor'},
 'date': 1475716876,
 'message_id': 38,
 'chat': {'id': 99999999,
         'last_name': 'Panunzio',
         'first_name': 'Victor',
         'type': 'private'}}

#Mensaje privado texto plano:
{'date': 1475716878,
 'text': 'lel',
 'message_id': 39,
 'chat': {'username': 'YiyiRojas',
          'id': 999999999,
          'first_name': 'Luigi',
          'type': 'private'},
 'from': {'username': 'YiyiRojas',
         'id': 999999999,
         'first_name': 'Luigi'}}

#Mensaje grupo texto plano:
{'date': 1475769348,
 'chat': {'all_members_are_administrators': False,
          'type': 'group',
          'title': 'AI Testing Lab.',
          'id': -999999999},
 'text': 'testing',
 'from': {'first_name': 'Luigi',
           'username': 'YiyiRojas',
           'id': 999999999},
           'message_id': 88}

#Mensaje grupo comando de bot:
{'message_id': 93,
 'date': 1475769683,
 'from': {'last_name': 'Panunzio',
          'id': 999999999,
          'first_name': 'Victor'},
 'chat': {'type': 'group',
          'id': -999999999,
          'title': 'AI Testing Lab.',
          'all_members_are_administrators': False},
'entities': [{'offset': 0,
            'type': 'bot_command',
            'length': 5}],
'text': '/help'}

}
