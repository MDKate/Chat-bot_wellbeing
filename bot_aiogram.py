import pandas as pd
import numpy as np
import emoji
import datetime
import  asyncio
import os
import pathlib
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from SQL import db_start, create_profile, logs_insert, edit_profile, count_value_from_db, city_value_from_db, page_value_from_db, ChoosingTopicsResult_value_from_db, firstResult_value_from_db, endSlinding_value_from_db, slindingResult_value_from_db, nextPage_value_from_db, nextPage1_value_from_db,nextPageDS_value_from_db,SecondResult_value_from_db,endSecond_value_from_db,slindingType5Result_value_from_db, s_value_from_db, cep_value_from_db, typGen_value_from_db, cepType_value_from_db, SlidingLevelTupe4Result_value_from_db, all_table_from_db

# Подключаемся к боту
botMes = Bot(open(os.path.abspath('token.txt')).read())
bot = Dispatcher(botMes)

# Скачиваем таблицу состояний
global tree
tree = pd.read_excel(os.path.abspath("tree.xlsx"))
del (tree['Unnamed: 0'])

# Подключаемся к БД
async def on_startup(_):
    await db_start()
    df = await all_table_from_db(table_name_db='base')
    buttons = [['Вернуться к выбору раздела', 'Помощь']]
    markupRK = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)

    for i in range(0, len(df)):
        if df['replay_button'][i] is None:
            await botMes.send_message(text='У нас обновление! Теперь в клавиатуре есть волшебные кнопочки!😊', chat_id=df['user_id'][i], reply_markup=markupRK)
            await edit_profile(name='replay_button', value=1, user_id=df['user_id'][i])


# Создаем глобальные переменные
# global count
# global city
# global page
# global ChoosingTopicsResult
# global firstResult
# global endSlinding
# global slindingResult
# global nextPage
# global nextPage1
# global nextPageDS
# global SecondResult
# global SlidingLevelTupe4Result
# global endSecond
# global slindingType5Result
# global s
# global logs1
# global cep
# global typGen
# global cepType


# Реагируем на нажатие на кнопки
@bot.callback_query_handler()
async def callback_query(callback: types.CallbackQuery, tree=tree) :
#     Перехватываем ID нажатой кнопки
    call = callback
    req = call.data.split('_')
    # print(req[0])


    # Считываем из БД значения переменных
    count = await count_value_from_db(call.message.chat.id)
    count = int(count)
    city = await city_value_from_db(call.message.chat.id)
    page = await page_value_from_db(call.message.chat.id)
    page = int(page)
    ChoosingTopicsResult = await ChoosingTopicsResult_value_from_db(call.message.chat.id)
    if len(str(ChoosingTopicsResult)) >5:
        ChoosingTopicsResult = str(ChoosingTopicsResult).split(',')
    firstResult = await firstResult_value_from_db(call.message.chat.id)
    if len(str(firstResult)) > 5:
        firstResult = str(firstResult).split(',')
    endSlinding = await endSlinding_value_from_db(call.message.chat.id)
    slindingResult = await slindingResult_value_from_db(call.message.chat.id)
    if len(str(slindingResult)) > 5:
        slindingResult = str(slindingResult).split(',')
    nextPage = await nextPage_value_from_db(call.message.chat.id)
    nextPage1 = await nextPage1_value_from_db(call.message.chat.id)
    nextPageDS = await nextPageDS_value_from_db(call.message.chat.id)
    SecondResult = await SecondResult_value_from_db(call.message.chat.id)
    if len(str(SecondResult)) > 5:
        SecondResult = str(SecondResult).split(',')
    SlidingLevelTupe4Result = await SlidingLevelTupe4Result_value_from_db(call.message.chat.id)
    if len(str(SlidingLevelTupe4Result)) > 5:
        SlidingLevelTupe4Result = str(SlidingLevelTupe4Result).split(',')
    endSecond = await endSecond_value_from_db(call.message.chat.id)
    slindingType5Result = await slindingType5Result_value_from_db(call.message.chat.id)
    if len(str(slindingType5Result)) > 5:
        slindingType5Result = str(slindingType5Result).split(',')
    s = await s_value_from_db(call.message.chat.id)
    s = int(s)
    cep = await cep_value_from_db(call.message.chat.id)
    typGen = await typGen_value_from_db(call.message.chat.id)
    cepType = await cepType_value_from_db(call.message.chat.id)

    # Запись логов действий пользователя в базу
    await logs_insert(call.message.chat.id, str(datetime.datetime.now().date()), str(datetime.datetime.now().time()), req[0])


    # Определяем функции состояний
    def ChoosingTopics(tree):
        TopicName = np.array([str(tree['Name'][0:1][0]), 0])  # Заполняем первое значение первым именем ветки
        for i in range(1, len(tree)):  # Бежим по всей таблице
            if int(tree['FirstLevel'][i - 1:i]) != int(
                    tree['FirstLevel'][i:i + 1]):  # Если текущая строка означает другую ветку, то
                TopicName = np.append(TopicName, tree['Name'][i:i + 1])  # Записать имя новой ветки
                TopicName = np.append(TopicName, str(i))  # Записываем ссылку на координаты
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
        for i in range(int(start) + 1, int(end)):
            if int(tree['SecondLevel'][i - 1:i]) != int(
                    tree['SecondLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                FirstName = np.append(FirstName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                FirstName = np.append(FirstName, str(i))  # Записываем ссылку на координаты
        return FirstName, end

    def SlidingLevel(tree, firstResult, first, endSlinding):
        firstResult = pd.Series(firstResult)
        start1 = (firstResult.loc[lambda x: (x == first)].index)[0]
        # start1 = int(np.argwhere(firstResult == first))  # Определяем индекс выбранной кнопки
        start = int(firstResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(firstResult):
            end = endSlinding
        else:
            end = int(firstResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        SlidingLevelName = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(int(start) + 1, int(end) + 1):
            if int(tree['ThirdLevel'][i - 1:i]) != int(
                    tree['ThirdLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                SlidingLevelName = np.append(SlidingLevelName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                SlidingLevelName = np.append(SlidingLevelName, str(i))  # Записываем ссылку на координаты
        return SlidingLevelName  # заглушка

    def SecondLevel(tree, firstResult, first, endSlinding):
        firstResult = pd.Series(firstResult)
        start1 = (firstResult.loc[lambda x : (x==first)].index)[0] # Определяем индекс выбранной кнопки
        start = int(firstResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(firstResult):
            end = endSlinding
        else:
            end = int(firstResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        SecondName = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(int(start) + 1, int(end) + 1):
            if int(tree['ThirdLevel'][i - 1:i]) != int(
                    tree['ThirdLevel'][i:i + 1]):  # Есди это другая ветка внутри ветки
                SecondName = np.append(SecondName, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
                SecondName = np.append(SecondName, str(i))  # Записываем ссылку на координаты
        endSecond = end
        return SecondName, endSecond

    def SlidingLevelTupe4(tree, SecondResult, Second, endSecond):
        SecondResult = pd.Series(SecondResult)
        start1 = (SecondResult.loc[lambda x: (x == Second)].index)[0]  # Определяем индекс выбранной кнопки
        start = int(SecondResult[start1 + 1]) + 1  # Определяем первую строку отсчета для выбранной ветки
        if start1 + 2 == len(SecondResult):
            end = endSecond
        else:
            end = int(SecondResult[start1 + 3]) - 1  # Определяем последнюю строку отсчета для выбранной ветки
        slidNameType4 = np.array(
            [np.array(tree['Name'][start:start + 1])[0], start])  # Записываем первое имя ветки в этой ветке
        for i in range(int(start) + 1, int(end) + 1):
            slidNameType4 = np.append(slidNameType4, tree['Name'][i:i + 1])  # Дописываем имя новой ветки
            slidNameType4 = np.append(slidNameType4, str(i))  # Записываем ссылку на координаты
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
            slidNameType4 = np.append(slidNameType4, str(i))  # Записываем ссылку на координаты
        return slidNameType4  # заглушка

    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Начало работы----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    if req[0] == 'start':  # Если метка start

        ChoosingTopicsResult = ChoosingTopics(tree) # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(ChoosingTopicsResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=ChoosingTopicsResult[i],
                                            callback_data=str(int(i / 2))))  # Создаем соответствующие кнопки
        await botMes.edit_message_text(emoji.emojize(f"Выберите раздел: :magnifying_glass_tilted_left: "), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page = 0
        count = 0
        # Сохраняем переменные в БД
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult) # Функция преобразования массива в строку
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('count', count, call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка чат для общения----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '5':  # Если метка 5
        ChoosingTopicsResult = ChoosingTopics(tree) # Вызываем функцию
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        markup.add(InlineKeyboardButton(text=firstResult[0], url='https://t.me/+IrCCc6c5d9hmNjYy'))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(f"А вот и ссылочка на чат для общения) 	:smiling_face_with_heart-eyes:"),
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        firstResult = ','.join(firstResult)
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка секции----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '6':  # Если метка 6
        ChoosingTopicsResult = ChoosingTopics(tree)  # Вызываем функцию
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(
                InlineKeyboardButton(text=firstResult[i],
                                     callback_data='Sect' + str(i / 2)))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(
            f"Выберите город, для которого вы хотите узнать расписание работы секций) :woman_swimming:"),
            reply_markup=markup, chat_id=call.message.chat.id,
            message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        firstResult = ','.join(firstResult)
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)

    elif 'Sect' in req[0]:  # Детализация списка секций по выбранному городу
        sectCity = firstResult[int(float(req[0][4:])) * 2]  # Определяем выбранный город
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        # print(os.path.abspath(pathlib.Path("Секции", f"{str(sectCity)}.PNG")), 'rb')
        await call.message.answer_photo(
            open(os.path.abspath(pathlib.Path("Секции", f"{str(sectCity)}.PNG")), 'rb'))  # Отправляем фото с  расписанием работы секций
        markup.add(InlineKeyboardButton(text='Вернуться к выбору города',
                                        callback_data='6'))  # Создаем кнопку возврата на главную страницу
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        # print(call.message.message_id)
        await botMes.edit_message_text(emoji.emojize(
            f"Вот расписание для города {sectCity}:woman_swimming:"),
            reply_markup=markup, message_id=call.message.message_id, chat_id=call.message.chat.id)  # Выводим сопутствующее сообщение
        await botMes.send_message(text=emoji.emojize(f"Вот расписание для города {sectCity}:woman_swimming:"),
            reply_markup=markup,  chat_id=call.message.chat.id)


    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка - СГУ на спорте----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '0':  # Если метка 0
        ChoosingTopicsResult = ChoosingTopics(tree) # Вызываем функцию
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='next-page' + str(i / 2)))  # Создаем соответствующие кнопки
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(f"Выберите тему: 	:flexed_biceps:"), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page = 0
        s = 0
        # Сохраняем переменные в БД
        firstResult = ','.join(firstResult)
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)

    elif 'next-page' in req[0]:  # Если метка содержит next-page
        if s == 1:  # Определяем направление движения
            page = page + 2
        nextPage = req[0]  # Запоминаем нажатую кнопку
        slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][9:])) * 2],
                                      endSlinding)  # Вызываем функцию
        count = len(slindingResult)
        s = 0
        if page < count:  # Если движемся вперед
            markup = InlineKeyboardMarkup()  # Определяем кнопку
            markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'back-page'),
                       InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                       # Создаем кнопку назад
                       InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                            callback_data=req[0]))  # Создаем кнопку вперед
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[0]}"',
                                            callback_data='0'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
            await botMes.edit_message_text(f'<a href="{str(slindingResult[page])}">Проосмотр видео: </a>',
                                           parse_mode=types.ParseMode.HTML, reply_markup=markup,
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            # if s==0:
            page = page + 2
        # Сохраняем переменные в БД
        slindingResult = ','.join(slindingResult)
        await edit_profile('nextPage', nextPage, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)
        await edit_profile('slindingResult', slindingResult, call.message.chat.id)
        await edit_profile('count', count, call.message.chat.id)

    elif req[0] == 'back-page':  # Если движемся назад
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
            await botMes.edit_message_text(f'<a href="{str(slindingResult[page])}">Проосмотр видео: </a>', parse_mode=types.ParseMode.HTML,
                                            reply_markup=markup, chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка ДМС----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '4':  # Если метка 4
        ChoosingTopicsResult = ChoosingTopics(tree) # Вызываем функцию
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='type3' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(f"Какое ДМС вас интересует? :man_health_worker:"), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        nextPage = 'type3' + str(i / 2)  # Запоминаем нажатую кнопку
        page = 0
        # Сохраняем переменные в БД
        firstResult = ','.join(firstResult)
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
        await edit_profile('nextPage', nextPage, call.message.chat.id)

    elif 'type3' in req[0]:  # Промежуточный шаг для двух типов ДМС (общий - типы, стоматология - города)
        cep = req[0]   #Запоминаем текущую кнопку
        if page == 0: #Если идем первый раз
            SecondResult, endSecond = SecondLevel(tree, firstResult,
                                          firstResult[int(float(req[0][5:]) * 2)],
                                          endSlinding)  # Вызываем функцию
            nextPage1 = req[0]  # Запоминаем нажатую кнопку
        else: #Если это повторное обращение
            SecondResult, endSecond = SecondLevel(tree, firstResult,
                                          firstResult[int(float(req[0][5:]) * 2)],
                                          endSlinding)  # Вызываем функцию от предыдущей кнопки
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(SecondResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=SecondResult[i],
                                    callback_data='typDS3' + str(
                                        i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[8]}"',
                                callback_data='4'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(f"Что вас интересует? \n Ваш выбор: \n {firstResult[int(float(req[0][5:]) * 2)]}", reply_markup=markup,
                               chat_id=call.message.chat.id,
                               message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page += 1
        # Сохраняем переменные в БД
        nextPageDS = 'typeDS' + str(i / 2)  # Запоминаем нажатую кнопку
        SecondResult = ','.join(SecondResult)
        await edit_profile('SecondResult', SecondResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('endSecond', endSecond, call.message.chat.id)
        await edit_profile('nextPage1', nextPage1, call.message.chat.id)
        await edit_profile('nextPageDS', nextPageDS, call.message.chat.id)
        await edit_profile('cep', cep, call.message.chat.id)

    elif  'typDS3' in req[0] and cep == 'type30.0': #Если идем по ветке общего ДМС
        cepType = req[0] #Запоминаем нажатую кнопку
        SlidingLevelTupe4Result = SlidingLevelTupe4(tree, SecondResult,
                                                        SecondResult[int(float(req[0][6:])) * 2], endSecond) #Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(SlidingLevelTupe4Result), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=SlidingLevelTupe4Result[i],
                                                callback_data='typDScity' + str(
                                                    i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться к типу помощи',
                                            callback_data=cep)) #Кнопка возврата к типу помощи
        markup.add(InlineKeyboardButton(text='Вернуться к типу ДМС',
                                            callback_data='4')) #Кнопка возврата к ДМС
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(f'Выберите ваш город: \n Ваш выбор: \n {firstResult[int(float(cep[5:]) * 2)]} \n {SecondResult[int(float(req[0][6:])) * 2]}', parse_mode='Markdown', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        typGen = 'typGen' + str(i / 2)  # Запоминаем нажатую кнопку
        # Сохраняем переменные в БД
        SlidingLevelTupe4Result = ','.join(SlidingLevelTupe4Result)
        await edit_profile('SlidingLevelTupe4Result', SlidingLevelTupe4Result, call.message.chat.id)
        await edit_profile('typGen', typGen, call.message.chat.id)
        await edit_profile('cep', cep, call.message.chat.id)
        await edit_profile('cepType', cepType, call.message.chat.id)

    elif 'typDS3' in req[0] and "type31.0" in nextPage1: # Если мы выбрали город в стоматологии
        cepType = req[0] # Запоминаем нажатую кнопку
        listTable = pd.read_excel(
            os.path.abspath(pathlib.Path("ДМС", f"{SecondResult[int(float(req[0][6:])) * 2]}", "Стоматология.xlsx"))) # Выбираем нужный файл


        markup = InlineKeyboardMarkup()
        for i in range(0, len(listTable)):
        # for i in range(0, 1):
            if pd.isna(listTable['Телефон'][i]) == True: listTable['Телефон'][i] = " "
            if pd.isna(listTable['Наименование медицинской организации'][i]) == True: listTable['Наименование медицинской организации'][i] = " "
            if pd.isna(listTable['Адрес медицинской организации'][i]) == True: listTable['Адрес медицинской организации'][i] = " "
            markup.add(InlineKeyboardButton(text=str(listTable['Наименование медицинской организации'][i] + " " +
                                                     listTable['Адрес медицинской организации'][i] + " "
                                                     + listTable['Телефон'][i]), url=listTable['Сайт'][i])) # Создаем кнопки для каждой клиники
        markup.add(InlineKeyboardButton(text=f'Полный список клиник',
                                            callback_data='obs'))  # Создаем кнопку возврата на главную страницу
        markup.add(InlineKeyboardButton(text='Вернуться к типу ДМС',
                                        callback_data='4')) # Кнопка возврата к типу ДМС
        markup.add(InlineKeyboardButton(text='Вернуться к выбору города',
                                        callback_data=cep)) # Кнопка возврата к выбору города
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(f'Клиники: \n Ваш выбор: \n {firstResult[int(float(cep[5:]) * 2)]} \n {SecondResult[int(float(req[0][6:])) * 2]}', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        await edit_profile('cepType', cepType, call.message.chat.id)

    elif 'typDScity' in req[0]: # Если выбран город в ветке общего ДМС
        listTable = pd.read_excel(os.path.abspath(pathlib.Path("ДМС", f"{SlidingLevelTupe4Result[int(float(req[0][9:])*2)]}", f"{SecondResult[int(float(cepType[6:])*2)]}.xlsx"))) # Получаем нужный файл
        city = req[0] # Запоминаем значение текущей кнопки
        markup = InlineKeyboardMarkup() # Создаем клавиатуру
        for i in range(0, len(listTable)):
            if pd.isna(listTable['Телефон'][i]) == True: listTable['Телефон'][i] = " "
            if pd.isna(listTable['Наименование медицинской организации'][i]) == True: listTable['Наименование медицинской организации'][i] = " "
            if pd.isna(listTable['Адрес медицинской организации'][i]) == True: listTable['Адрес медицинской организации'][i] = " "
            markup.add(InlineKeyboardButton(text=str(listTable['Наименование медицинской организации'][i] + " " + listTable['Адрес медицинской организации'][i] + " "
                      + listTable['Телефон'][i]), url=listTable['Сайт'][i])) # Создаем кнопки для каждой клиники

        markup.add(InlineKeyboardButton(text=f'Полный список клиник',
                                        callback_data=f'clinic'))  # Создаем кнопку возврата на главную страницу
        markup.add(InlineKeyboardButton(text='Вернуться к типу помощи',
                                        callback_data=cep)) # Кнопка возврата к типу помощи
        markup.add(InlineKeyboardButton(text='Вернуться к выбору города',
                                        callback_data=cepType)) # Кнопка возврата к выбору города
        markup.add(InlineKeyboardButton(text='Вернуться к типу ДМС',
                                        callback_data='4')) # Кнопка возврата к ДМС
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(f"Клиники: \n Ваш выбор: \n {firstResult[int(float(cep[5:]) * 2)]} \n {SecondResult[int(float(cepType[6:])) * 2]} \n {SlidingLevelTupe4Result[int(float(req[0][9:])*2)]}", reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id) # Отправляем соответствующее сообщение
        # Сохраняем переменные в БД
        await edit_profile('city', city, call.message.chat.id)

    elif 'clinic' in req[0]: # Если отправляем файл для общего ДМС
        pth = os.path.abspath(pathlib.Path("ДМС", f"{SlidingLevelTupe4Result[int(float(city[9:])*2)]}", "Общий.xlsx"))
        await botMes.send_document(call.message.chat.id, open((pth), 'rb'))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Вернуться к типу помощи',
                                        callback_data=cep))  # Кнопка возврата к типу помощи
        markup.add(InlineKeyboardButton(text='Вернуться к выбору города',
                                        callback_data=cepType))  # Кнопка возврата к выбору города
        markup.add(InlineKeyboardButton(text='Вернуться к типу ДМС',
                                        callback_data='4'))  # Кнопка возврата к ДМС
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.send_message(text=f'Вернуться к выбору:', reply_markup=markup, chat_id=call.message.chat.id)

    elif req[0] == 'obs': # Если отправляем файл для стоматологии
        f = open(pathlib.Path("ДМС", f"{SecondResult[int(float(cepType[6:])) * 2]}", "Общий.xlsx"), "rb")
        await botMes.send_document(call.message.chat.id, f)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Вернуться к типу помощи',
                                        callback_data=cep))  # Кнопка возврата к типу помощи
        markup.add(InlineKeyboardButton(text='Вернуться к выбору города',
                                        callback_data=cepType))  # Кнопка возврата к выбору города
        markup.add(InlineKeyboardButton(text='Вернуться к типу ДМС',
                                        callback_data='4'))  # Кнопка возврата к ДМС
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.send_message(text=f'Вернуться к выбору:', reply_markup=markup, chat_id=call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка ГТО----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '3':  # Если метка 3
        ChoosingTopicsResult = ChoosingTopics(tree) #Вызываем функцию
        page = 0
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='type4' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text('Для какой категории вас интересуют нормы ГТО? \n'+'<a href="https://www.gto.ru/norms"> [Ссылочка на официальный сайт]</a>',
                                                     parse_mode=types.ParseMode.HTML, reply_markup=markup,
                                                     chat_id=call.message.chat.id,
                                                     message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        firstResult = ','.join(firstResult)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)

    elif 'type4' in req[0]:  # Выбор возрастной группы
        if page == 0:
            SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:]) * 2)],
                                                      endSlinding)  # Вызываем функцию
            nextPage1 = req[0]  # Запоминаем нажатую кнопку

        else:
            SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[(int(float(nextPage1[5:])) * 2)],
                                                      endSlinding)  # Вызываем функцию от предыдущей кнопки
            page -= 1

        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(SecondResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=SecondResult[i],
                                                callback_data='typ4' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text=f'Вернуться к группам',
                                            callback_data='3'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await  botMes.edit_message_text(f"Для какой возрастной группы вас интересуют нормы ГТО?", reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        page += 1
        # Сохраняем переменные в БД
        SecondResult = ','.join(SecondResult)
        await edit_profile('SecondResult', SecondResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('endSecond', endSecond, call.message.chat.id)
        await edit_profile('nextPage1', nextPage1, call.message.chat.id)

    elif 'typ4' in req[0]:  # Ссылка на файл ПДФ
        slindingResult = SlidingLevel(tree, SecondResult, SecondResult[int(float(req[0][4:])) * 2],
                                          endSecond)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку

        markup.add(InlineKeyboardButton(text=f'Вернуться к "{firstResult[int(float(nextPage1[5:])) * 2]}"',
                                            callback_data='type4'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text=f'Вернуться к к группам',
                                            callback_data='3'))  # Создаем кнопку возврата к теме
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                            callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text('Нормы ГТО: '+f'<a href="{str(slindingResult[0])}">[Ссылочка на PDF]</a>',
                                           parse_mode=types.ParseMode.HTML,
                                           chat_id=call.message.chat.id, reply_markup=markup,
                                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        slindingResult = ','.join(slindingResult)
        await edit_profile('slindingResult', slindingResult, call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка фитлекции----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '2':  # Если метка 3
        ChoosingTopicsResult = ChoosingTopics(tree) # Вызываем функцию
        page = 0
        firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
                                              ChoosingTopicsResult)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(firstResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=firstResult[i],
                                            callback_data='name1' + str(i / 2)))  # Создаем соответствующую кнопку
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(f"Какую лекцию вы хотите послушать? :television:"), reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        s = 0
        # Сохраняем переменные в БД
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)
        firstResult = ','.join(firstResult)
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, call.message.chat.id)
        await edit_profile('firstResult', firstResult, call.message.chat.id)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('endSlinding', endSlinding, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)

    # elif 'name10.0' == req[0]:  # Если это проект Здоровая спина
    #     slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
    #                                       endSlinding)  # Вызываем функцию
    #     markup = InlineKeyboardMarkup()  # Определяем кнопку
    #     markup.add(
    #             InlineKeyboardButton(text=slindingResult[0], url='https://vk.com/'))  # Создаем соответствующую кнопку
    #     markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
    #                                         callback_data='2'))  # Создаем кнопку возврата к теме
    #     markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                         callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #     await botMes.edit_message_text(f'Ссылка на проект "Здоровая спина":', reply_markup=markup, chat_id=call.message.chat.id,
    #                               message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    #     # Сохраняем переменные в БД
    #     slindingResult = ','.join(slindingResult)
    #     await edit_profile('slindingResult', slindingResult, call.message.chat.id)

    # elif 'name10.0' != req[0] and 'name1' in req[0]:  # Если это видео - идем вперед (для 3 подразделов)
    elif 'name10.0' == req[0]: # Если это видео - идем вперед
        if s == 1:  # Определяем направление движения
            page = page + 2
        nextPage = req[0]  # Запоминаем нажатую кнопку
        slindingResult = SlidingLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
                                          endSlinding)  # Вызываем функцию
        count = len(slindingResult)
        s = 0
        if page < count:  # Если движемся вперед
            markup = InlineKeyboardMarkup()  # Определяем кнопку
            # markup.add(
            #         InlineKeyboardButton(text=slindingResult[page], callback_data=req[0]))  # Создаем соответствующую кнопку
            markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage1'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=req[0]))  # Создаем кнопку вперед
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
                                                callback_data='2'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
            # await botMes.edit_message_text(f'Проосмотр видео:', reply_markup=markup, chat_id=call.message.chat.id,
            #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            await botMes.edit_message_text(f'<a href="{str(slindingResult[page])}">Проосмотр видео: </a>',
                                           parse_mode=types.ParseMode.HTML, reply_markup=markup,
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            page = page + 2
        # Сохраняем переменные в БД
        slindingResult = ','.join(slindingResult)
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)
        await edit_profile('count', count, call.message.chat.id)
        await edit_profile('slindingResult', slindingResult, call.message.chat.id)
        await edit_profile('nextPage', nextPage, call.message.chat.id)

    elif req[0] == 'backpage1':  # Если это видео - идем назад
        if s == 0:  # Определяем направление движения
            page = page - 2
        s = 1
        if page > 1:  # Если движемся назад
            page = page - 2
            markup = InlineKeyboardMarkup()  # Определяем кнопку
            # markup.add(InlineKeyboardButton(text=slindingResult[page],
            #                                     callback_data=nextPage))  # Создаем соответствующую кнопку
            markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage1'),
                           InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
                       # Создаем кнопку назад
                           InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
                                                callback_data=nextPage))  # Создаем кнопку вперед
            markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[4]}"',
                                                callback_data='2'))  # Создаем кнопку возврата к теме
            markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                                callback_data='start'))  # Создаем кнопку возврата на главную страницу
            # await botMes.edit_message_text(f'Проосмотр видео:', reply_markup=markup, chat_id=call.message.chat.id,
            #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
            await botMes.edit_message_text(f'<a href="{str(slindingResult[page])}">Проосмотр видео: </a>',
                                           parse_mode=types.ParseMode.HTML, reply_markup=markup,
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
        # Сохраняем переменные в БД
        await edit_profile('page', page, call.message.chat.id)
        await edit_profile('s', s, call.message.chat.id)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Ветка пропитание----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    elif req[0] == '1':  # Если метка 1
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        markup.add(InlineKeyboardButton(text="Ссылка", url="https://здоровое-питание.рф/")) # Кнопка со ссылкой на сайт
        markup.add(InlineKeyboardButton(text='Вернуться на главную',
                                        callback_data='start'))  # Создаем кнопку возврата на главную страницу
        await botMes.edit_message_text(emoji.emojize(f"Здесь вы можете подробнее узнать про правильное питание! :face_savoring_food:"),
                              reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)  # Выводим сопутствующее сообщение

    # На будущее:
    # elif 'name20.0' == req[0]:  # Если метка содержит name20.0
    #     SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
    #                                           endSlinding)  # Вызываем функцию
    #     markup = InlineKeyboardMarkup()  # Определяем кнопку
    #     markup.add(InlineKeyboardButton(text=SecondResult[0], callback_data=f' '))  # Создаем соответствующую кнопку
    #     markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
    #                                     callback_data='1'))  # Создаем кнопку возврата к теме
    #     markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                     callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #     bot.edit_message_text(f"Это помощник. Он выдает один произвольный рецепт. Ваш рецепт:", reply_markup=markup,
    #                           chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # elif 'name20.0' != req[0] and 'name2' in req[0]:  # Если метка не содержит name20.0 и содержит name2
    #     if page == -1:
    #         SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(req[0][5:])) * 2],
    #                                               endSlinding)  # Вызываем функцию
    #     else:
    #         SecondResult, endSecond = SecondLevel(tree, firstResult, firstResult[int(float(nextPage1[5:]) * 2)],
    #                                               endSlinding)  # Вызываем функцию по предыдущей кнопке
    #     markup = InlineKeyboardMarkup()  # Определяем кнопку
    #     for i in range(0, len(SecondResult), 2):  # Бежим по списку, вовзвращенному функцией
    #         markup.add(InlineKeyboardButton(text=SecondResult[i],
    #                                         callback_data='type5' + str(i / 2)))  # Создаем соответствующую кнопку
    #     markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
    #                                     callback_data='1'))  # Создаем кнопку возврата к теме
    #     markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                     callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #     bot.edit_message_text(f"Выберите калорийность:", reply_markup=markup, chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    #     nextPage1 = req[0]  # Запоминаем нажатую кнопку
    #     page = 0
    #     s = 0
    # elif 'type5' in req[0]:  # Если метка содержит type5
    #     if 'ChoosingTopicsResult' in globals():
    #         if s == 1:  # Определяем направление движения
    #             page = page + 2
    #         nextPage = req[0]  # Запоминаем нажатую кнопку
    #         slindingType5Result = SlidingLevelTupe5(tree, SecondResult, SecondResult[int(float(req[0][5:])) * 2],
    #                                                 endSecond)  # Вызываем функцию
    #         count = len(slindingType5Result)
    #         s = 0
    #         if page < count:  # Если движемся вперед
    #             markup = InlineKeyboardMarkup()  # Определяем кнопку
    #             markup.add(InlineKeyboardButton(text=slindingType5Result[page],
    #                                             callback_data=req[0]))  # Создаем соответствующую кнопку
    #             markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage2'),
    #                        InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
    #                        # Создаем кнопку назад
    #                        InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
    #                                             callback_data=req[0]))  # Создаем кнопку вперед
    #             markup.add(InlineKeyboardButton(text=f'Вернуться к "Калорийность"',
    #                                             callback_data=nextPage1))  # Создаем кнопку возврата к теме
    #             markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
    #                                             callback_data='1'))  # Создаем кнопку возврата к теме
    #             markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                             callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #             bot.edit_message_text(f'Рецепты: ', reply_markup=markup, chat_id=call.message.chat.id,
    #                                   message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    #             page = page + 2
    #     else:
    #         markup = InlineKeyboardMarkup()
    #         markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
    #         bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
    #                               reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    # elif req[0] == 'backpage2':  # Если метка  backpage2
    #     if 'ChoosingTopicsResult' in globals():
    #         if s == 0:  # Определяем направление движения
    #             page = page - 2
    #         s = 1
    #         if page > 1:  # Если движемся назад
    #             page = page - 2
    #             markup = InlineKeyboardMarkup()  # Определяем кнопку
    #             markup.add(InlineKeyboardButton(text=slindingType5Result[page],
    #                                             callback_data=f' '))  # Создаем соответствующую кнопку
    #             markup.add(InlineKeyboardButton(text=emoji.emojize(f':left_arrow: Назад'), callback_data=f'backpage2'),
    #                        InlineKeyboardButton(text=f'{int(page / 2) + 1}/{int(count / 2)}', callback_data=f' '),
    #                        # Создаем кнопку назад
    #                        InlineKeyboardButton(text=emoji.emojize(f'Вперёд :right_arrow:'),
    #                                             callback_data=nextPage))  # Создаем кнопку вперед
    #             markup.add(InlineKeyboardButton(text=f'Вернуться к "Калорийность"',
    #                                             callback_data=nextPage1))  # Создаем кнопку возврата к теме
    #             markup.add(InlineKeyboardButton(text=f'Вернуться к "{ChoosingTopicsResult[2]}"',
    #                                             callback_data='1'))  # Создаем кнопку возврата к теме
    #             markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                             callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #             bot.edit_message_text(f'Рецепты:', reply_markup=markup, chat_id=call.message.chat.id,
    #                                   message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    #     else:
    #         markup = InlineKeyboardMarkup()
    #         markup.add(InlineKeyboardButton(text=emoji.emojize('Начать :detective:'), callback_data='start'))
    #         bot.edit_message_text(emoji.emojize(f'Я немного подучился :desktop_computer: и готов помогать вам дальше! :man_running: Давайте снова начнем общаться! :e-mail:'),
    #                               reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)  # Выводим сопутствующее сообщение



# Обработчик входящих сообщений
@bot.message_handler(commands=['start'])  # Начинаем работу
async def start(message: types.message):
    global count
    global page
    markup = InlineKeyboardMarkup()  # Определяем кнопку
    markup.add(InlineKeyboardButton(text=f'Начнем', callback_data=f'start')) # Создаем кнопку старта
    await message.reply(emoji.emojize(
        "Добрый день!:hand_with_fingers_splayed: Вы хотите узнать что-то про ЗОЖ?:red_question_mark: Тогда, нажмите кнопку: :play_button:"),
                    reply_markup=markup)  # Выводим сопутствующее сообщение
    # Создаем в БД строку для нового человека (старого - перезаписываем)
    await create_profile(user_id=message.from_user.id)
    buttons = [['Вернуться к выбору раздела', 'Помощь']]
    markupRK = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)

    df = await all_table_from_db(table_name_db='base')
    # print((df[df['user_id'] == str(message.chat.id)]['replay_button']).values[0])
    if (df[df['user_id'] == str(message.chat.id)]['replay_button']).values[0] != 1:
            await botMes.send_message(text='У нас обновление! Теперь в клавиатуре есть волшебные кнопочки!😊',
                                      chat_id=message.chat.id, reply_markup=markupRK)
            await edit_profile(name='replay_button', value=1, user_id=message.chat.id)



@bot.message_handler()  # Обрабатываем текстовые сообщения
async def start(message: types.message, tree=tree):

    def ChoosingTopics(tree):
        TopicName = np.array([str(tree['Name'][0:1][0]), 0])  # Заполняем первое значение первым именем ветки
        for i in range(1, len(tree)):  # Бежим по всей таблице
            if int(tree['FirstLevel'][i - 1:i]) != int(
                    tree['FirstLevel'][i:i + 1]):  # Если текущая строка означает другую ветку, то
                TopicName = np.append(TopicName, tree['Name'][i:i + 1])  # Записать имя новой ветки
                TopicName = np.append(TopicName, str(i))  # Записываем ссылку на координаты
        return TopicName

    count = await count_value_from_db(message.chat.id)
    count = int(count)
    page = await page_value_from_db(message.chat.id)
    page = int(page)
    ChoosingTopicsResult = await ChoosingTopicsResult_value_from_db(message.chat.id)
    if len(str(ChoosingTopicsResult)) > 5:
        ChoosingTopicsResult = str(ChoosingTopicsResult).split(',')




    if message.text == 'Вернуться к выбору раздела':
        ChoosingTopicsResult = ChoosingTopics(tree)  # Вызываем функцию
        markup = InlineKeyboardMarkup()  # Определяем кнопку
        for i in range(0, len(ChoosingTopicsResult), 2):  # Бежим по списку, вовзвращенному функцией
            markup.add(InlineKeyboardButton(text=ChoosingTopicsResult[i],
                                            callback_data=str(int(i / 2))))  # Создаем соответствующие кнопки
        await botMes.send_message(text=emoji.emojize(f"Выберите раздел: :magnifying_glass_tilted_left: "),
                                       reply_markup=markup,
                                       chat_id=message.chat.id)  # Выводим сопутствующее сообщение
        page = 0
        count = 0
        # Сохраняем переменные в БД
        ChoosingTopicsResult = ','.join(ChoosingTopicsResult)  # Функция преобразования массива в строку
        await edit_profile('ChoosingTopicsResult', ChoosingTopicsResult, message.chat.id)
        await edit_profile('page', page, message.chat.id)
        await edit_profile('count', count, message.chat.id)
    elif message.text == 'Помощь':
        await botMes.send_message(text='Если вам необходима консультация 🧐 или у вас что-то сломалось 😱, вы можете написать о своей проблеме в чат техподдержки ⚙: <a href="https://t.me/+90xxSovog65lMjM6">Чат техподдержки</a>', chat_id=message.chat.id, parse_mode=types.ParseMode.HTML)
    else:
        await message.reply(emoji.emojize(
        "Увы! :weary_face: Я умею общаться только кнопками(	:woman_facepalming: Поэтому, пожалуйста, напишите мне /start, чтобы снова начать общение! :beating_heart:"))  # Выводим сопутствующее сообщение

if __name__ == '__main__':
    # Бесконечно запускаем бот и игнорим ошибки
    while True:
        try:
            executor.start_polling(bot, on_startup=on_startup)
        except:
            pass
