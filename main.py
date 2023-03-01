#!/srv/blago/env/bin/python3

import telebot
import telegram
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
import numpy as np
import emoji
from pathlib import Path
from telegram import ParseMode
import datetime
import os

from emoji import emojize

# Подключаемся к боту
bot = telebot.TeleBot('')


page = 1
count = 10


# Определяем отклик
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    global count
    global page
    global ChoosingTopicsResult
    global firstResult
    global endSlinding
    global slindingResult
    global nextPage
    global nextPage1
    global SecondResult
    global endSecond
    global slindingType5Result
    global s
    global logs1

    try:
        logs1 = pd.read_csv(os.path.abspath('Statistic.csv'))
        del (logs1['Unnamed: 0'])
        time1 = str(datetime.datetime.now().time())
        dat1 = str(datetime.datetime.now().date())
        logs1 = logs1.concat({'date': dat1, 'time': time1, 'person_id': call.message.chat.id, 'branch_id': req[0]},
                             ignore_index=True)
        path2 = os.path.abspath("Statistic.csv")
        logs1.to_csv(path2)
    except:
        pass

    # Скачиваем таблицу состояний
    global tree
    path1 = os.path.abspath("tree.xlsx")
    tree = pd.read_excel(path1)
    del (tree['Unnamed: 0'])

    # Определяем функции состояний
    def ChoosingTopics(tree):
        TopicName = np.array([str(tree['Name'][0:1][0]), 0])  # Заполняем первое значение первым именем ветки
        for i in range(1, len(tree)):  # Бежим по всей таблице
            if int(tree['FirstLevel'][i - 1:i]) != int(
                    tree['FirstLevel'][i:i + 1]):  # Если текущая строка означает другую ветку, то
                TopicName = np.append(TopicName, tree['Name'][i:i + 1])  # Записать имя новой ветки
                TopicName = np.append(TopicName, i)  # Записываем ссылку на координаты
        return TopicName

    def FirstLevel(tree, choos, ChoosingTopicsResult):
        start1 = int(np.argwhere(ChoosingTopicsResult == choos))  # Определяем индекс выбранной кнопки
        start = int(ChoosingTopicsResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(ChoosingTopicsResult):
            end = len(tree)
        else:
            end = int(ChoosingTopicsResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        FirstName = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(start + 1, end):
            if int(tree['SecondLevel'][i - 1:i]) != int(
                    tree['SecondLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                FirstName = np.append(FirstName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                FirstName = np.append(FirstName, i)  # Записываем ссылку на координаты
        return FirstName, end

    def SlidingLevel(tree, firstResult, first, endSlinding):
        start1 = int(np.argwhere(firstResult == first))  # Определяем индекс выбранной кнопки
        start = int(firstResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(firstResult):
            end = endSlinding
        else:
            end = int(firstResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        SlidingLevelName = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(start + 1, end + 1):
            if int(tree['ThirdLevel'][i - 1:i]) != int(
                    tree['ThirdLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                SlidingLevelName = np.append(SlidingLevelName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                SlidingLevelName = np.append(SlidingLevelName, i)  # Записываем ссылку на координаты
        return SlidingLevelName  # заглушка

    def SecondLevel(tree, firstResult, first, endSlinding):
        start1 = int(np.argwhere(firstResult == first))  # Определяем индекс выбранной кнопки
        start = int(firstResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(firstResult):
            end = endSlinding
        else:
            end = int(firstResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        SecondName = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(start + 1, end + 1):
            if int(tree['ThirdLevel'][i - 1:i]) != int(
                    tree['ThirdLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                SecondName = np.append(SecondName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                SecondName = np.append(SecondName, i)  # Записываем ссылку на координаты
        endSecond = end
        return SecondName, endSecond

    def SlidingLevelTupe4(tree, SecondResult, Second, endSecond):
        start1 = int(np.argwhere(SecondResult == Second))  # Определяем индекс выбранной кнопки
        start = int(SecondResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(SecondResult):
            end = endSecond
        else:
            end = int(SecondResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        slidNameType4 = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(start + 1, end + 1):
            slidNameType4 = np.append(slidNameType4, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
            slidNameType4 = np.append(slidNameType4, i)  # Записываем ссылку на координаты
        return slidNameType4  # заглушка

    def SlidingLevelTupe5(tree, SecondResult, Second, endSecond):
        start1 = int(np.argwhere(SecondResult == Second))  # Определяем индекс выбранной кнопки
        start = int(SecondResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(SecondResult):
            end = endSecond
        else:
            end = int(SecondResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        slidNameType4 = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(start + 1, end + 1):
            slidNameType4 = np.append(slidNameType4, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
            slidNameType4 = np.append(slidNameType4, i)  # Записываем ссылку на координаты
        return slidNameType4  # заглушка

    # Объявляем глобальные переменные



    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Начало работы----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    if req[0] == 'start':  # Если метка start
        ChoosingTopicsResult = ChoosingTopics(tree)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(ChoosingTopicsResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=ChoosingTopicsResult[i],
                                            callback_data=str(int(i / 2))))  # Создаем соответствующие кнопки
        bot.edit_message_text(emoji.emojize(f"Выберите раздел: :magnifying_glass_tilted_left: "), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page = 0
        count = 0
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка чат для общения----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '5':  # Если метка 5
        ChoosingTopicsResult = ChoosingTopics(tree)
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        markup.add(InlineKeyboardButton(text=firstResult[0], url='https://vk.com/'))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(f"А вот и ссылочка на чат для общения) 	:smiling_face_with_heart-eyes:"),
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка секции----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '6':  # Если метка 6
        ChoosingTopicsResult = ChoosingTopics(tree)
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(
                InlineKeyboardButton(text=firstResult[i], callback_data=str(i / 2)))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(
            f"У нас для вас есть целая карта секций, на который вы можете выбрать то, что интересует вас больше всего) :woman_swimming:"),
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка - СГУ на спорте----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '0':  # Если метка 0
        ChoosingTopicsResult = ChoosingTopics(tree)
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='next-page' + str(i / 2)))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(f"Выберите тему: 	:flexed_biceps:"), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page = 0
        s = 0
    elif 'next-page' in req[0]:  # Если метка содержит next-page
        if 'ChoosingTopicsResult' in globals():
            if s == 1:  # Определяем направление движения
                page = page + 2
            nextPage = req[0]  # Запоминаем нажатую кнопку
            slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][9:])) * 2],
                                        endSlinding)  # Вызываем функцию
            count = len(slindingResult)
            s = 0
            if page < count:  # Если движемся вперед
                markup = InlineKeyboardMarkup()  # Определяем кнопку
            # bot.send_message(chat_id=call.message.chat.id, text=str(slindingResult[page]),
            #                                 parse_mode=ParseMode.HTML)

                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'back-page'),
                        InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                       # Создаем кнопку назад
                        InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=req[0]))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[0]}"',
                                                callback_data='0'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Проосмотр видео: {str(slindingResult[page])}',parse_mode=ParseMode.HTML, reply_markup=markup, chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            # if s==0:
                page = page + 2
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif req[0] == 'back-page':  # Если метка содержит back-page
        if 'ChoosingTopicsResult' in globals():
            if s == 0:  # Определяем направление движения
                page = page - 2
            s = 1
            if page > 1:  # Если движемся назад
                page = page - 2
                markup = InlineKeyboardMarkup()  # Определяем кнопку
                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'back-page'),
                        InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                       # Создаем кнопку назад
                        InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=nextPage))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[0]}"',
                                                callback_data='0'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Проосмотр видео: {str(slindingResult[page])}',parse_mode=ParseMode.HTML, reply_markup=markup, chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка ДМС----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '4':  # Если метка 4
        ChoosingTopicsResult = ChoosingTopics(tree)
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        # for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
        #     markup.add(InlineKeyboardButton(text=firstResult[i],
        #                                     callback_data='type3' + str(i / 2)))  # Создаем соответствующую кнопку
        bot.send_message(call.message.chat.id, emoji.emojize(
            "Идет загрузка. Пожалуйста, подождите!"), reply_markup=markup)
        bot.send_document(call.message.chat.id, os.path.abspath("/Клиники.xlsx"))
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        markup.add(InlineKeyboardButton(text=f'Начнем', callback_data=f'start'))
        bot.send_message(call.message.chat.id, emoji.emojize(
            "Добрый день!:hand_with_fingers_splayed: Вы хотите узнать что-то про ЗОЖ?:red_question_mark: Тогда, нажмите кнопку: :play_button:"),
                         reply_markup=markup)






        # markup.add(InlineKeyboardButton(text='Вернуться на главную',
        #                                 callback_data='start'))  # Создаем кнопку возврата на главную страницу
        # bot.edit_message_text(emoji.emojize(f"Какое ДМС вас интересует? :man_health_worker:"), reply_markup=markup,
        #                       chat_id=call.message.chat.id,
        #                       message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # nextPage = 'type3' + str(i / 2)  # Запоминаем нажатую кнопку
    # elif 'type3' in req[0]:  # Если метка содержит type3
    #     bot.send_document(call.message.chat.id, open(r"C:/Users/50AdmNsk/Downloads/Клиники.xlsx", 'rb'))

        # slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(nextPage[5:])) * 2],
        #                               endSlinding)  # Вызываем функцию
        # markup = InlineKeyboardMarkup()  # Определяем кнопку
        # markup.add(
        #     InlineKeyboardButton(text=slindingResult[0], url='https://vk.com/'))  # Создаем соответствующую кнопку
        # markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[8]}"',
        #                                 callback_data='4'))  # Создаем кнопку возврата к теме
        # markup.add(InlineKeyboardButton(text='Вернуться на главную',
        #                                 callback_data='start'))  # Создаем кнопку возврата на главную страницу
        # bot.edit_message_text(f"Информация по ДМС:", reply_markup=markup, chat_id=call.message.chat.id,
        #                       message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка ГТО----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '3':  # Если метка 3
        ChoosingTopicsResult = ChoosingTopics(tree)
        page = 0
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='type4' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(f"Для какой категории вас интересуют нормы ГТО? :man_cartwheeling:\n [Ссылочка на официальный сайт](https://www.gto.ru/norms)"), parse_mode='Markdown',
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif 'type4' in req[0]:  # Если метка содержит type4
        if 'ChoosingTopicsResult' in globals():
            if page == 0:
                SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:]) * 2)],
                                                      endSlinding)  # Вызываем функцию
                nextPage1 = req[0]  # Запоминаем нажатую кнопку
            else:
                SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(nextPage1[5:]) * 2)],
                                                      endSlinding)  # Вызываем функцию от предыдущей кнопки
            markup = InlineKeyboardMarkup()  # Определяем кнопку
            for i in range(0, len(SecondResult), 2):  # Бежим по списку, вовзвращенному функцией
                markup.add(InlineKeyboardButton(text=SecondResult[i],
                                                callback_data='typ4' + str(i / 2)))  # Создаем соответствующую кнопку
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[6]}"',
                                            callback_data='3'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
            bot.edit_message_text(f"Для какой возрастной группы вас интересуют нормы ГТО?", reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            page += 1
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif 'typ4' in req[0]:  # Если метка содержит typ4
        if 'ChoosingTopicsResult' in globals():
            slindingResult = SlidingLevel(tree, SecondResult, SecondResult[int(float(req[0][4:])) * 2],
                                          endSecond)  # Вызываем функцию
            markup = InlineKeyboardMarkup()  # Определяем кнопку

            markup.add(InlineKeyboardButton(text=f'Вернуться к "{firstResult[int(float(nextPage1[5:])) * 2]}"',
                                            callback_data='type4'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[6]}"',
                                            callback_data='3'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
            bot.edit_message_text(f'Нормы ГТО: [Ссылочка на PDF]({str(slindingResult[0])})', parse_mode='Markdown', reply_markup=markup,
                                   chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка фитлекции----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '2':  # Если метка 3
        ChoosingTopicsResult = ChoosingTopics(tree)
        page = 0
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='name1' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(f"Какую лекцию вы хотите послушать? :television:"), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        s = 0
    elif 'name10.0' == req[0]:  # Если метка содержит name10.0
        if 'ChoosingTopicsResult' in globals():
            slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
                                          endSlinding)  # Вызываем функцию
            markup = InlineKeyboardMarkup()  # Определяем кнопку
            markup.add(
                InlineKeyboardButton(text=slindingResult[0], url='https://vk.com/'))  # Создаем соответствующую кнопку
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
                                            callback_data='2'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
            bot.edit_message_text(f'Ссылка на проект "Здоровая спина":', reply_markup=markup, chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif 'name10.0' != req[0] and 'name1' in req[0]:  # Если метка не содержит name10.0
        if 'ChoosingTopicsResult' in globals():
            if s == 1:  # Определяем направление движения
                page = page + 2
            nextPage = req[0]  # Запоминаем нажатую кнопку
            slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
                                          endSlinding)  # Вызываем функцию
            count = len(slindingResult)
            s = 0
            if page < count:  # Если движемся вперед
                markup = InlineKeyboardMarkup()  # Определяем кнопку
                markup.add(
                    InlineKeyboardButton(text=slindingResult[page], callback_data=req[0]))  # Создаем соответствующую кнопку
                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage1'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                           # Создаем кнопку назад
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=req[0]))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
                                                callback_data='2'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Проосмотр видео:', reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)  # Выводим сопутствующее сообщение
                page = page + 2
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif req[0] == 'backpage1':  # Если метка backpage1
        if 'ChoosingTopicsResult' in globals():
            if s == 0:  # Определяем направление движения
                page = page - 2
            s = 1
            if page > 1:  # Если движемся назад
                page = page - 2
                markup = InlineKeyboardMarkup()  # Определяем кнопку
                markup.add(InlineKeyboardButton(text=slindingResult[page],
                                                callback_data=nextPage))  # Создаем соответствующую кнопку
                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage1'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                       # Создаем кнопку назад
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=nextPage))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
                                                callback_data='2'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Проосмотр видео:', reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка пропитание----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '1':  # Если метка 1
        ChoosingTopicsResult = ChoosingTopics(tree)
        page = -1
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='name2' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(emoji.emojize(f"Какой рецеп вы хотите получить? :face_savoring_food:"),
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение

    elif 'name20.0' == req[0]:  # Если метка содержит name20.0
        SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
                                              endSlinding)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        markup.add(InlineKeyboardButton(text=SecondResult[0], callback_data=f' '))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
                                        callback_data='1'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(f"Это помощник. Он выдает один произвольный рецепт. Ваш рецепт:", reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif 'name20.0' != req[0] and 'name2' in req[0]:  # Если метка не содержит name20.0 и содержит name2
        if page == -1:
            SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
                                                  endSlinding)  # Вызываем функцию
        else:
            SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(nextPage1[5:]) * 2)],
                                                  endSlinding)  # Вызываем функцию по предыдущей кнопке
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(SecondResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=SecondResult[i],
                                            callback_data='type5' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
                                        callback_data='1'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        bot.edit_message_text(f"Выберите калорийность:", reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        nextPage1 = req[0]  # Запоминаем нажатую кнопку
        page = 0
        s = 0
    elif 'type5' in req[0]:  # Если метка содержит type5
        if 'ChoosingTopicsResult' in globals():
            if s == 1:  # Определяем направление движения
                page = page + 2
            nextPage = req[0]  # Запоминаем нажатую кнопку
            slindingType5Result = SlidingLevelTupe5(tree, SecondResult, SecondResult[int(float(req[0][5:])) * 2],
                                                    endSecond)  # Вызываем функцию
            count = len(slindingType5Result)
            s = 0
            if page < count:  # Если движемся вперед
                markup = InlineKeyboardMarkup()  # Определяем кнопку
                markup.add(InlineKeyboardButton(text=slindingType5Result[page],
                                                callback_data=req[0]))  # Создаем соответствующую кнопку
                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage2'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                           # Создаем кнопку назад
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=req[0]))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "Калорийность"',
                                                callback_data=nextPage1))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
                                                callback_data='1'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Рецепты: ', reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)  # Выводим сопутствующее сообщение
                page = page + 2
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    elif req[0] == 'backpage2':  # Если метка  backpage2
        if 'ChoosingTopicsResult' in globals():
            if s == 0:  # Определяем направление движения
                page = page - 2
            s = 1
            if page > 1:  # Если движемся назад
                page = page - 2
                markup = InlineKeyboardMarkup()  # Определяем кнопку
                markup.add(InlineKeyboardButton(text=slindingType5Result[page],
                                                callback_data=f' '))  # Создаем соответствующую кнопку
                markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage2'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                           # Создаем кнопку назад
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=nextPage))  # Создаем кнопку вперед
                markup.add(InlineKeyboardButton(text=f'Вернуться к "Калорийность"',
                                                callback_data=nextPage1))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
                                                callback_data='1'))  # Создаем кнопку возврата к теме
                markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
                bot.edit_message_text(f'Рецепты:', reply_markup=markup, chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
            bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
                                  reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение



# Обработчик входящих сообщений
@bot.message_handler(commands=['start'])  # Начинаем работу

def start(m):

    global count
    global page
    markup = InlineKeyboardMarkup()  # Определяем кнопку
    markup.add(InlineKeyboardButton(text=f'Начнем', callback_data=f'start'))
    bot.send_message(m.from_user.id, emoji.emojize(
        "Добрый день!:hand_with_fingers_splayed: Вы хотите узнать что-то про ЗОЖ?:red_question_mark: Тогда, нажмите кнопку: :play_button:"),
                    reply_markup=markup)  # Выводим сопутствующее сообщение


@bot.message_handler()  # Обрабатываем текстовые сообщения

def start(m):
    bot.send_message(m.from_user.id, emoji.emojize(
        "Увы! :weary_face: Я умею общаться только кнопками(	:woman_facepalming: Поэтому, пожалуйста, напишите мне /start, чтобы снова начать общение! :beating_heart:"))  # Выводим сопутствующее сообщение

if __name__ == '__main__':

    bot.polling(none_stop=True)










