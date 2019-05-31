import vk_api
import random
import time

token = 'hidden'

vk = vk_api.VkApi(token=token)

vk._auth_token()

keyboard_yes_no = '{"one_time": true,\
"buttons": [[{"action": {"type": "text","label": "Да"}, "color": "positive"},\
{"action": {"type": "text","label": "Нет"},"color": "negative"}]]}'

keyboard_chosen_tribe = '{"one_time": true,\
"buttons": [[{"action": {"type": "text","label": "Отлично!"}, "color": "primary"},\
{"action": {"type": "text","label": "Уже есть это племя."},"color": "default"}]]}'

tribes = ('Kickoo', 'Hoodrick', 'Luxidoor', 'Vengir', 'Zebasi', 'Ai-Mo', 'Quetzali', 'Yădakk', 'Aquarion', '∑∫ỹriȱŋ')

q1 = {'type': 'subs',
      'text': 'В игре для вас главное - победа?',
      'yes': (2, 5, 1, 10, 4, 7, 9, 3, 8, 6),
      'next_yes': 2,
      'no': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
      'next_no': 5}
q2 = {'type': 'subs',
      'text': 'Вы предпочитаете игры на 5+ человек дуэлям?',
      'yes': (4, 6, 1, 9, 3, 8, 7, 2, 10, 5),
      'next_yes': 3,
      'no': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
      'next_no': 4}
q3 = {'type': 'subs',
      'text': 'Вы любите игры на 9+ человек?',
      'yes': (6, 8, 1, 3, 5, 9, 4, 7, 10, 2),
      'next_yes': 4,
      'no': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
      'next_no': 4}
q4 = {'type': 'incr',
      'text': 'Вы готовы заплатить за племя больше 75 рублей?',
      'yes': (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
      'next_yes': 0,
      'no': (0, 0, 30, 0, 0, 0, 0, 0, 30, 30),
      'next_no': 0}
q5 = {'type': 'incr',
      'text': 'Постепенному выстраиванию экономики вы предпочитаете быструю атаку на врага?',
      'yes': (2, 0, -4, -4, 0, 4, 2, -2, -2, -4),
      'next_yes': 6,
      'no': (-2, 0, 0, 4, -2, -2, -2, 0, 0, +2),
      'next_no': 6}
q6 = {'type': 'incr',
      'text': 'Вам нужен стабильный доход в начале игры, даже если это вредит другим аспектам игры?',
      'yes': (-3, 1, -3, 3, -3, 1, 1, 1, 3, 1),
      'next_yes': 7,
      'no': (1, -3, 1, -1, +1, -1, -1, -1, -1, -3),
      'next_no': 7}
q7 = {'type': 'incr',
      'text': 'Вы предпочитаете новые и интересные игровые механики стабильному развитию?',
      'yes': (0, 0, 0, 0, 0, 0, 0, 0, -10, -10),
      'next_yes': 4,
      'no': (0, 0, 0, 0, 0, 0, 0, 0, +2, +2),
      'next_no': 4}
questions = (q1, q2, q3, q4, q5, q6, q7)

users = {}


def ask_yes_no(number, user_id):
    vk.method('messages.send', {'peer_id': user_id,
                                'message': questions[number-1]['text'],
                                'keyboard': keyboard_yes_no,
                                'random_id': random.randint(1, 2147483647)})


def ask_chosen_tribe(tribe_number, user_id):
    vk.method('messages.send', {'peer_id': user_id,
                                'message': 'Ваш выбор: ' + tribes[tribe_number],
                                'keyboard': keyboard_chosen_tribe,
                                'random_id': random.randint(1, 2147483647)})


def end(user_id):
    vk.method('messages.send', {'peer_id': user_id,
                                'message': 'Вот и славно.',
                                'random_id': random.randint(1, 2147483647)})

def bad_end(user_id):
    vk.method('messages.send', {'peer_id': user_id,
                                'message': 'Мы перебрали все племена :)',
                                'random_id': random.randint(1, 2147483647)})

while True:
    try:
        messages = vk.method('messages.getConversations', {'offset': 0, 'count': 20, 'filter': 'unanswered'})
        if messages['count'] > 0:
            id = messages['items'][0]['last_message']['from_id']
            body = messages['items'][0]['last_message']['text']
            if id not in users.keys():
                users[id] = {'current_question': -1, 'tribe_rating': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
            if body.lower() in ('выбор племени', '\"выбор племени\"'):
                users[id]['current_question'] = 1
                ask_yes_no(1, id)
            if users[id]['current_question'] > 0:
                if body.lower() == 'да':
                    if questions[users[id]['current_question']-1]['type'] == 'subs':
                        for i in range(len(users[id]['tribe_rating'])):
                            users[id]['tribe_rating'][i] = questions[users[id]['current_question']-1]['yes'][i]
                    else:
                        for i in range(len(users[id]['tribe_rating'])):
                            users[id]['tribe_rating'][i] += questions[users[id]['current_question']-1]['yes'][i]
                    users[id]['current_question'] = questions[users[id]['current_question'] - 1]['next_yes']
                    if users[id]['current_question'] != 0:
                        ask_yes_no(users[id]['current_question'], id)
                    else:
                        ask_chosen_tribe(users[id]['tribe_rating'].index(min(users[id]['tribe_rating'])), id)
                if body.lower() == 'нет':
                    if questions[users[id]['current_question'] - 1]['type'] == 'subs':
                        for i in range(len(users[id]['tribe_rating'])):
                            users[id]['tribe_rating'][i] += questions[users[id]['current_question']-1]['no'][i]
                            # да, это костыль, ответ "нет" будет прибавлять, даже если тип вопроса - subs
                            # иначе пришлось бы вводить тип каждому ответу, а мне немного лень
                            # впрочем, TODO
                    else:
                        for i in range(len(users[id]['tribe_rating'])):
                            users[id]['tribe_rating'][i] += questions[users[id]['current_question']-1]['no'][i]
                    users[id]['current_question'] = questions[users[id]['current_question'] - 1]['next_no']
                    if users[id]['current_question'] != 0:
                        ask_yes_no(users[id]['current_question'], id)
                    else:
                        ask_chosen_tribe(users[id]['tribe_rating'].index(min(users[id]['tribe_rating'])), id)
            else:
                if body.lower() == 'отлично!':
                    users[id] = {'current_question': -1, 'tribe_rating': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
                    end(id)
                elif body.lower() == 'уже есть это племя.':
                    users[id]['tribe_rating'][users[id]['tribe_rating'].index(min(users[id]['tribe_rating']))] = 100
                    if min(users[id]['tribe_rating']) < 100:
                        ask_chosen_tribe(users[id]['tribe_rating'].index(min(users[id]['tribe_rating'])), id)
                    else:
                        bad_end(id)

    except Exception as E:
        time.sleep(1)
