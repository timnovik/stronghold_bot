import xlwings
import vk_api
from setup import token, n_lands, n_lords, n_feods, admines
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import *
from functions import get_row, get_lord, get_data1


def id(s):
    return vk.users.get(user_ids=s)[0]['id']


def name(id):
    return vk.users.get(user_ids=id, fields='screen_name')[0]['screen_name']


def is_admine(id):
    return name(id) in admines or event.user_id in admines

print('authorizing')

vk_session = vk_api.VkApi(token=token)

print('receiving session')

longpoll = VkLongPoll(vk_session)

print('getting api')

vk = vk_session.get_api()

print('opening excel book')

book = xlwings.Book('data.xlsx')
sheet_lords = book.sheets[2]
sheet_lands = book.sheets[1]
sheet_feods = book.sheets[0]

print('initializing lords and lands')

lands = []
lords = []
feods = []

for i in range(2, n_feods + 2):
    row = get_row(sheet_feods, i, 'A', 'C')
    feods.append(Feod(row[0], int(row[1]), bool(int(row[2]))))
for i in range(2, n_lands + 2):
    row = get_row(sheet_lands, i, 'A', 'D')
    lands.append(Land(row[0], row[1], str(row[2]).split(','), row[3]))
for i in range(2, n_lords + 2):
    row = get_row(sheet_lords, i, 'A', 'F')
    if row[5] is not None:
        lords.append(King(row[0], int(row[1]), row[3], row[4], row[5]))
    else:
        lords.append(Lord(row[0], int(row[1]), row[2], row[3], row[4]))
get_data(lands, lords, feods)
get_data1(lands, lords, feods)
print('RUNNING')

collected_income = False

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        command = list(map(lambda x: x.lower(), event.text.split()))
        if command[0] == 'стоп':
            if event.from_user and is_admine(event.user_id):
                vk.messages.send(user_id=event.user_id, message='бот остановлен', random_id=0)
                break
        elif command[0] == 'id':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=str(event.user_id), random_id=0)
        elif command[0] == 'помощь' or command[0] == 'начать':
            if event.from_user:
                vk.messages.send(user_id=event.user_id, message=open('help.txt', encoding='utf-8').read(), random_id=0)
        elif command[0] == 'доход':
            if event.from_user and is_admine(event.user_id) and not collected_income:
                for i in range(len(lords)):
                    lord = lords[i]
                    lord.income()
                    sheet_lords.range(f'A{i + 2}:F{i + 2}').value = lords[i].list()
                collected_income = True
                book.save()
                vk.messages.send(user_id=event.user_id, message='доходы собраны',
                                 random_id=0)
                print("доходы начислены")
        elif command[0] == 'сводка':
            if event.from_user and is_admine(event.user_id):
                text = ''
                for i in range(len(lords)):
                    text += f'{i + 1}) {str(lords[i])}\n'
                vk.messages.send(user_id=event.user_id, message=text,
                                 random_id=0)
        elif command[0:2] == ['новый', 'ход']:
            if event.from_user and event.user_id in admines and collected_income:
                collected_income = False
        elif command[0] == 'заплатить':
            if event.from_user:
                for i in range(len(lords)):
                    lord = lords[i]
                    id = int(command[2])
                    j = lords.index(get_lord(id))
                    if lord.id == event.user_id:
                        if lord.pay(id, int(command[1])):
                            vk.messages.send(user_id=event.user_id, message=f'перевод учтен, у вас осталось {lord.money} монет', random_id=0)
                            sheet_lords.range(f'A{i + 2}:F{i + 2}').value = lord.list()
                            sheet_lords.range(f'A{j + 2}:F{j + 2}').value = lords[j].list()
                            book.save()
                        else:
                            vk.messages.send(user_id=event.user_id, message=f'перевод не учтен, у вас недостаточно средств. Если это не так, обратитесь к администрации.', random_id=0)
        elif command[0:2] == ['мои', 'деньги']:
            if event.from_user:
                for lord in lords:
                    if lord.id == event.user_id:
                        vk.messages.send(user_id=event.user_id, message=f'у вас {lord.money} монет', random_id=0)
'''
sheet.range('C1').value = 1

book.save('table.xlsx')
'''