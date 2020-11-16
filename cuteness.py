import telebot
from telebot import types
import time

API_TOKEN = '1445172839:AAGaLI71L9LZvWCHh5c6LU3h5KiVF_7XyTU'

bot = telebot.TeleBot(API_TOKEN)


# Начало программы
@bot.message_handler(commands=["start"])
def start_func(message):
    # Клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Перейти на сайт 🌎")
    item2 = types.KeyboardButton("Узнать индекс массы тела (ИМС)")
    item3 = types.KeyboardButton("Расчет калорий")
    item4 = types.KeyboardButton("Определить тип кожи")
    item5 = types.KeyboardButton("Таймер")
    item6 = types.InlineKeyboardButton("Выбрать тренеровку")

    markup.add(item1, item2, item3, item4, item5, item6)

    # Первое сообщение
    bot.send_message(message.chat.id, "Приветствую тебя, {0.first_name}!\n"
                                      "Что бы ты хотел сделать?".format(message.from_user), parse_mode='html',
                     reply_markup=markup)


# Обработка нажатий по кнопкам
@bot.message_handler(content_types=["text"])
def open_google(message):
    if message.chat.type == 'private':
        if message.text == "Перейти на сайт 🌎":
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="https://www.google.com/")
            keyboard.add(url_button)
            bot.send_message(message.chat.id, "Нажми на кнопку чтобы перейти на сайт", reply_markup=keyboard)

        elif message.text == "Узнать индекс массы тела (ИМС)":

            # Массив хранения данных
            global array, arr_l
            array = []

            try:
                for i in range(len(array)):
                    array.pop(i)

            except Exception as e:
                print(repr(e))

            try:
                message = bot.send_message(message.chat.id, "Введите свой вес: ")
                flag = True
                i = 1
                g = 0
                while flag:
                    bot.register_next_step_handler(message, save_weight)
                    if len(array) == 0:
                        time.sleep(i)
                        i = 1
                        g += 1
                        # print(i)
                        if g > 10:
                            flag = False
                    else:
                        flag = False
                        time.sleep(2)
                        arr_l = len(array)
                        message = bot.send_message(message.chat.id, "Введите свой рост: ")
                flag2 = True
                i2 = 1
                g2 = 0
                while flag2:
                    if len(array) <= arr_l:
                        time.sleep(i2)
                        i2 = 1
                        g2 += 1
                        # print(i2)
                        if g2 > 10:
                            flag2 = False
                    else:
                        flag2 = False
                        time.sleep(0)
                        bot.register_next_step_handler(message, save_height)

                        index_mass = round(((array[0]) / (array[-1] ** 2)) * 10000, 1)

                        time.sleep(1)

                        # Вывод индекса массы тела
                        bot.send_message(message.chat.id, index_mass)

                        if index_mass < 18.5:
                            bot.send_message(message.chat.id, "ИМТ ниже нормального веса")
                        elif 18.5 <= index_mass < 25:
                            bot.send_message(message.chat.id, "Нормальный вес")
                        elif 25 <= index_mass < 30:
                            bot.send_message(message.chat.id, "Избыточный вес")
                        elif 30 < index_mass <= 35:
                            bot.send_message(message.chat.id, "Ожирение 1-ой степени")
                        elif 35 <= index_mass < 40:
                            bot.send_message(message.chat.id, "Ожирение 2-ой степени")
                        elif index_mass >= 40:
                            bot.send_message(message.chat.id, "Ожирение 3-ей степени")

                        bot.send_message(message.chat.id, "❗ Возможно следующая кнопка не сработает с первого раза")

            except Exception:
                bot.send_message(message.chat.id, "Ошибка!\nВозможно введены не все данные")

        elif message.text == "Определить тип кожи":
            bot.send_message(message.chat.id, "Хорошо, тогда давайте начнем")

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да", callback_data='yes')
            item2 = types.InlineKeyboardButton("Нет", callback_data='no')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Ваша кожа блестит, имеет расширенные поры\n"
                                              "и склонна к появлению черных точек и прыщей?", reply_markup=markup)

        elif message.text == 'Расчет калорий':
            global arAge
            arAge = []

            try:
                for i in range(len(arAge)):
                    arAge.pop(i)

            except Exception as e:
                print(repr(e))

            try:
                if len(array) > 2:

                    bot.send_message(message.chat.id, "Пожалуйста, укажите свой возвраст")
                    flag = True
                    i = 1
                    g = 0
                    while flag:
                        bot.register_next_step_handler(message, save_age)
                        if len(arAge) == 0:
                            time.sleep(i)
                            i = 1
                            g += 1
                            # print(i)
                            if g > 10:
                                flag = False
                        else:
                            flag = False
                            markup = types.InlineKeyboardMarkup(row_width=2)
                            item1 = types.InlineKeyboardButton("Мужчина", callback_data='m')
                            item2 = types.InlineKeyboardButton("Женщина", callback_data='w')

                            markup.add(item1, item2)

                            bot.send_message(message.chat.id, "Пожалуйста выберите пол", reply_markup=markup)

            except Exception as e:
                bot.send_message(message.chat.id, "Для начала нужно узнать ИМС!")

        if message.text == 'Таймер':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('10 сек', callback_data='10')
            item2 = types.InlineKeyboardButton('30 сек', callback_data='30')
            item3 = types.InlineKeyboardButton('1 минута', callback_data='1')
            item4 = types.InlineKeyboardButton('3 минуты', callback_data='3')
            item5 = types.InlineKeyboardButton('5 минут', callback_data='5')
            item6 = types.InlineKeyboardButton('10 минут', callback_data='100')

            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, "На сколько времени вы хотите поставить таймер?", reply_markup=markup)

        if message.text == 'Выбрать тренеровку':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('ВИИТ', callback_data='VIIT')
            item2 = types.InlineKeyboardButton('Зарядка',  callback_data='zar')
            item3 = types.InlineKeyboardButton('Кардио',  callback_data='kard')
            item4 = types.InlineKeyboardButton('Руки',  callback_data='hands')
            item5 = types.InlineKeyboardButton('Пресс',  callback_data='abs')
            item6 = types.InlineKeyboardButton('Ноги',  callback_data='foot')

            markup.add(item1, item2, item3, item4, item5, item6)

            bot.send_message(message.chat.id, "Выбери тип тенеровки", reply_markup=markup)

    # Исключение
    else:
        bot.send_message(message.chat.id, "Я не знаю что ответить 😔")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            # Если кожа жирная
            if call.data == 'yes':

                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Ваша кожа блестит, имеет расширенные поры и склонна к появлению черных точек и прыщей?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                bot.send_message(call.message.chat.id, "*Похоже у вас жирная кожа*", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "❗️Жирная кожа нуждается в матировании и косметике с"
                                                       " себорегулирующими и бактерицидными компонентами,"
                                                       " которые помогут избежать высыпаний!")
            elif call.data == 'no':
                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Ваша кожа блестит, имеет расширенные поры и склонна к появлению черных точек и прыщей?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Если кожа не жирная
                markup = types.InlineKeyboardMarkup(row_width=2)

                item1 = types.InlineKeyboardButton("Да", callback_data='yess')
                item2 = types.InlineKeyboardButton("Нет", callback_data='noo')

                markup.add(item1, item2)

                bot.send_message(call.message.chat.id, "Испытываете чуство стянутости полсе умывания, иногда шелушение?"
                                 , reply_markup=markup)
            # Если кожа сухая
            if call.data == 'yess':
                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Испытываете чуство стянутости полсе умывания, иногда шелушение?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                bot.send_message(call.message.chat.id, "*Похоже у вас сухая кожа*", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "❗️Сухая кожа нуждается в интенсивном увлажнении и питании:"
                                                       " ищите в составе мощные влагоудерживающие и"
                                                       " увлажняющие вещества.")

            if call.data == 'noo':
                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Испытываете чуство стянутости полсе умывания, иногда шелушение?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                # Создаем новую клавиатуру для комбинированной кожи
                markupT = types.InlineKeyboardMarkup(row_width=2)

                itemT1 = types.InlineKeyboardButton("Да", callback_data='yyes')
                itemT2 = types.InlineKeyboardButton("Нет", callback_data='nno')

                markupT.add(itemT1, itemT2)

                bot.send_message(call.message.chat.id,
                                 "В Т-зоне (нос, лоб, подбородок) блестит и жирнится,\n"
                                 "заметны расширенные поры и на щеках страдает от сухости?", reply_markup=markupT)

            # Если кожа комбинированная
            if call.data == 'yyes':
                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="В Т-зоне (нос, лоб, подбородок) блестит и жирнится,\n"
                                           "заметны расширенные поры и на щеках страдает от сухости?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                bot.send_message(call.message.chat.id, "*Видимо у вас комбинированная кожа*", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "❗️Комбинированная кожа нуждается в уходе, который будет"
                                                       " учитывать ее особенности: например, мультимаскинге.")

            if call.data == 'nno':
                # Удаление предыдущей кнопки
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="В Т-зоне (нос, лоб, подбородок) блестит и жирнится,\n"
                                           "заметны расширенные поры и на щеках страдает от сухости?",
                                      reply_markup=None)

                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)

                bot.send_message(call.message.chat.id, "Поздравляю!🥳\nУ вас здоровая кожа")

            # Расчет нормы калорий
            if call.data == 'm':
                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)
                m = round(88.36 + (13.4 * array[0]) + (4.8 * array[-1]) - (5.7 * arAge[0]), 1)
                bot.send_message(call.message.chat.id, "Ваша норма калорой " + str(m))

            if call.data == 'w':
                # Удаление сообщения с вопросом
                bot.delete_message(call.message.chat.id, call.message.message_id)
                m = round(447.6 + (9.2 * array[0]) + (3.1 * array[-1]) - (4.3 * arAge[0]), 1)
                bot.send_message(call.message.chat.id, "Ваша норма калорой " + str(m))

            # Таймер
            global times
            times = 1
            if call.data == '10':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:
                    time.sleep(times)
                    g += 1
                    if g > 10:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == '30':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:
                    time.sleep(times)
                    g += 1
                    if g > 30:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == '1':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:

                    time.sleep(times)
                    g += 1
                    if g > 60:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == '3':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:

                    time.sleep(times)
                    g += 1
                    if g > 180:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == '5':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:

                    time.sleep(times)
                    g += 1
                    if g > 300:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == '100':
                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Отмена", callback_data='close')

                markup.add(itemT1)
                bot.send_message(call.message.chat.id, "Нажмите для отмены", reply_markup=markup)

                f_plus = True
                g = 0
                while f_plus:

                    time.sleep(times)
                    g += 1
                    if g > 600:
                        bot.send_message(call.message.chat.id, "Время вышло⏱")
                        f_plus = False

            if call.data == 'close':
                times = 0

            if call.data == 'VIIT':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # Создаем новую клавиатуру для комбинированной кожи
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='next')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=Dr5jWhUacGw&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=5&t=567s", reply_markup=markup)

            if call.data == 'next':

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='nextt')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=IZaWksgybZM", reply_markup=markup)

            if call.data == 'nextt':

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=fG-p3lgTOa8")

            # Разминка
            if call.data == 'zar':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='nnext')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id,
                                 "https://www.youtube.com/watch?v=m_MedxYkoCA&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=15&t=207s", reply_markup=markup)

            if call.data == 'nnext':

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='nnnext')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=UpvF16UhaFo", reply_markup=markup)

            if call.data == 'nnnext':

                bot.send_message(call.message.chat.id,
                "https://the-challenger.ru/dvizhenie/trenirovki/5-prostyh-uprazhnenij-kotorye-podgotovyat-telo-k-trenirovke/")

            if call.data == 'kard':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='neext')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=t6mzd_aZI9c&t=634s", reply_markup=markup)

            if call.data == 'neext':

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='neeext')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id,
                                 "https://www.youtube.com/watch?v=UoC_O3HzsH0&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=21&t=158s", reply_markup=markup)

            if call.data == 'neeext':

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=GIlcZlhiOf4")

            if call.data == 'hands':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='nexxt')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "Приложение для тренеровки рук(Google Play) - " +
                "https://play.google.com/store/apps/details?id=armworkout.armworkoutformen.armexercises&hl=ru&gl=US\n"
                                 "\nApp Store " +
                        "https://apps.apple.com/us/app/%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8-%D0%B4%D0%BB%D1%8F-%D1%80%D1%83%D0%BA/id1357526464?l=ru", reply_markup=markup)

            if call.data == 'nexxt':
                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=zXLwlRGfCMQ&t=540s")

            # Пресс
            if call.data == 'abs':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='next1')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id,
                "https://www.youtube.com/watch?v=9p7-YC91Q74&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=19&t=419s", reply_markup=markup)

            if call.data == 'next1':

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='next2')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id,
                "https://www.youtube.com/watch?v=xb7ByyKCahs&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=8&t=301s", reply_markup=markup)

            if call.data == 'next2':

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='next3')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id,
                "https://www.youtube.com/watch?v=GJMIycrp2Rs&list=PLFsUWAdhvDeqlSaFR8W7tZc04yUz7bRcn&index=28&t=226s", reply_markup=markup)

            if call.data == 'next3':

                bot.send_message(call.message.chat.id, "Приложение для тренеровки рук(Google Play) - " +
                                 "https://play.google.com/store/apps/details?id=sixpack.sixpackabs.absworkout&hl=ru&gl=US\n"
                                 "\nApp Store " + "https://apps.apple.com/ru/app/%D0%BA%D1%83%D0%B1%D0%B8%D0%BA%D0%B8-%D1%82%D1%80%D0%B5%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0-%D0%B4%D0%BB%D1%8F-%D0%BF%D1%80%D0%B5%D1%81%D1%81%D0%B0/id1338655056")

            if call.data == 'foot':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Выбери тип тенеровки",
                                      reply_markup=None)

                # След тренеровка
                markup = types.InlineKeyboardMarkup(row_width=1)

                itemT1 = types.InlineKeyboardButton("Вперёд", callback_data='nextn')

                markup.add(itemT1)

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=-fKpU0J8BYc", reply_markup=markup)

            if call.data == 'nextn':

                bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=q0pX4TnQfPw")

    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка")


# Сохранение веса
def save_weight(message):
    try:
        array.append(int(message.text))
        # bot.send_message(message.chat.id, len(array))
        # bot.send_message(message.chat.id, message.text)
    except Exception as e:
        print(repr(e))


# Сохранение роста
def save_height(message):
    try:
        array.append(int(messagetext))
        # bot.send_message(message.chat.id, message.text)
    except Exception as e:
        print(repr(e))


# Сохранение веса
def save_age(message):
    try:
        arAge.append(int(message.text))
        # bot.send_message(message.chat.id, len(array))
        # bot.send_message(message.chat.id, message.text)
    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.polling(none_stop=True)
