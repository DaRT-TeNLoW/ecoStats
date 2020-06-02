from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from bs4 import BeautifulSoup
import requests

TG_TOKEN = "1192518431:AAEv04To8wW61T7PfELBC7MojO96BmQ7aow"

# callback - то, что телега будет присылать в бота при нажатии на кнопку
CALLBACK_BUTTON1_CHINA = "CALLBACK_BUTTON1_CHINA"
CALLBACK_BUTTON2_USA = "CALLBACK_BUTTON2_USA"
CALLBACK_BUTTON3_INDIA = "CALLBACK_BUTTON3_INDIA"
CALLBACK_BUTTON4_RUSSIA = "CALLBACK_BUTTON4_RUSSIA"
CALLBACK_BUTTON5_COAL = "CALLBACK_BUTTON5_COAL"
CALLBACK_BUTTON6_CO2 = "CALLBACK_BUTTON6_CO2"
CALLBACK_BUTTON7_COAL_16 = "CALLBACK_BUTTON7_COAL_16"
CALLBACK_BUTTON8_COAL_15 = "CALLBACK_BUTTON8_COAL_15"
CALLBACK_BUTTON9_COAL_14 = "CALLBACK_BUTTON9_COAL_14"
CALLBACK_BUTTON10_COAL_13 = "CALLBACK_BUTTON10_COAL_13"
CALLBACK_BUTTON11_CO2_18 = "CALLBACK_BUTTON11_CO2_18"
CALLBACK_BUTTON12_CO2_14 = "CALLBACK_BUTTON12_CO2_14"

TITLES = {
    CALLBACK_BUTTON1_CHINA: "Китай",
    CALLBACK_BUTTON2_USA: "США",
    CALLBACK_BUTTON3_INDIA: "Индия",
    CALLBACK_BUTTON4_RUSSIA: "Россия",
    CALLBACK_BUTTON5_COAL: "Годовая добыча угля",
    CALLBACK_BUTTON6_CO2: "Эмиссия CO2",
    CALLBACK_BUTTON7_COAL_16: "2016",
    CALLBACK_BUTTON8_COAL_15: "2016 - 2015",
    CALLBACK_BUTTON9_COAL_14: "2016 - 2014",
    CALLBACK_BUTTON10_COAL_13: "2016 - 2013",
    CALLBACK_BUTTON11_CO2_18: "2018",
    CALLBACK_BUTTON12_CO2_14: "2018, 2014",
}
'''трёхмерный массив: первый уровень - тип данных (уголь, СО2)  <-- первое число
                      Второй уровень - страна (Китай, США, Индия, Россия)  <-- второе число
                      Третий уровень - год (2016, 2015, 2014, 2013):уголь;   (2018, 2014): СО2;  <-- третее число
                      
                     Пример: information[0][2][1] - уголь, Индия, 2015
                             information[1][0][0]
'''
                #добыча угля
information = [[["1.1", "2.1", "3.1", "4.1"],  #Китай
                ["5.1", "6.1", "7.1", "8.1"],  #США
                ["9.1", "10.1", "11.1", "12.1"],  #Индия
                ["13.1", "14.1", "15.1", "16.1"]],  #Россия
                #ємиссия СО2
               [["1", "2"],  #Китай
                ["3", "4"],  #США
                ["5", "6"],  #Индия
                ["7", "8"]]]  #Россия


# COAL
coal_data = requests.get("https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D1%80%D0%B0%D0%BD_%D0%BF%D0%BE_%D0%B4%D0%BE%D0%B1%D1%8B%D1%87%D0%B5_%D1%83%D0%B3%D0%BB%D1%8F")
coal_soup = BeautifulSoup(coal_data.text, "html.parser")
# container CSS-selector (Coal):
coal_rows = coal_soup.find("table", attrs={"class": "wikitable"}).find("tbody").find_all("tr")


for j in range(4):
    key = 2
    if j == 2:
        key = 1
    else:
        key = 2
    for i in range(4):
        information[0][j][i] = coal_rows[(j+1)*key].find_all("td")[(i + 1) * 2].getText()

# CO2
CO2_data = requests.get("https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D1%80%D0%B0%D0%BD_%D0%BF%D0%BE_%D1%8D%D0%BC%D0%B8%D1%81%D1%81%D0%B8%D0%B8_CO2")
CO2_soup = BeautifulSoup(CO2_data.text, "html.parser")
# container CSS-selector (CO2):
CO2_rows = CO2_soup.find_all("table", attrs={"class": "wikitable"})

# 0-st table with class 'wikitable', 1-st 'tr'(country) tag, 2-nd 'td'(value) tag
for i in range(4):
    information[1][i][0] = CO2_rows[0].find_all("tr")[i+1].find_all("td")[2].getText()

for j in range(4):
    information[1][j][1] = CO2_rows[1].find_all("tr")[j+1].find_all("td")[2].getText()

print(information)


countryid = 0
country = 0
type = 0
typen = ""


# клавиатура кнопок со странами
def get_keyboard1():
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_CHINA], callback_data=CALLBACK_BUTTON1_CHINA),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_USA], callback_data=CALLBACK_BUTTON2_USA),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_INDIA], callback_data=CALLBACK_BUTTON3_INDIA),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_RUSSIA], callback_data=CALLBACK_BUTTON4_RUSSIA),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# клавиатура кнопок с областями статистики
def get_keyboard2():
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_COAL], callback_data=CALLBACK_BUTTON5_COAL),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_CO2], callback_data=CALLBACK_BUTTON6_CO2),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# клавиатура кнопок с годами добычи угля
def get_keyboard3():
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_COAL_16], callback_data=CALLBACK_BUTTON7_COAL_16),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_COAL_15], callback_data=CALLBACK_BUTTON8_COAL_15),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_COAL_14], callback_data=CALLBACK_BUTTON9_COAL_14),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON10_COAL_13], callback_data=CALLBACK_BUTTON10_COAL_13),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# клавиатура кнопок с годами по СО2
def get_keyboard4():
    # Каждый список внутри `keyboard` -- это один горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец.
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON11_CO2_18], callback_data=CALLBACK_BUTTON11_CO2_18),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON12_CO2_14], callback_data=CALLBACK_BUTTON12_CO2_14),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(bot: Bot, update: Update):
    """ Обработчик ВСЕХ кнопок со ВСЕХ клавиатур
    """
    query = update.callback_query
    data = query.data
    global type
    global typen
    global countryid
    global country

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON1_CHINA:

        countryid = 0
        country = "Китай"
        query.edit_message_text(
            text="Статистику по каким данным вы бы хотели посмотреть у Китая?",
            reply_markup=get_keyboard2()
        )
    elif data == CALLBACK_BUTTON2_USA:

        countryid = 1
        country = "США"
        query.edit_message_text(
            text="Статистику по каким данным вы бы хотели посмотреть у США?",
            reply_markup=get_keyboard2()
        )
    elif data == CALLBACK_BUTTON3_INDIA:

        countryid = 2
        country = "Индия"
        query.edit_message_text(
            text="Статистику по каким данным вы бы хотели посмотреть у Индии?",
            reply_markup=get_keyboard2()
        )
    elif data == CALLBACK_BUTTON4_RUSSIA:

        countryid = 3
        country = "Россия"
        query.edit_message_text(
            text="Статистику по каким данным вы бы хотели посмотреть у России?",
            reply_markup=get_keyboard2()
        )

    elif data == CALLBACK_BUTTON5_COAL:

        type = 0
        typen = "Годовая добыча угля"
        query.edit_message_text(
            text="Выберете предложенные года, за которые вы хотите увидеть статистику:",
            reply_markup=get_keyboard3()
        )
    elif data == CALLBACK_BUTTON6_CO2:

        type = 1
        typen = "Годовая эмиссия СО2"
        query.edit_message_text(
            text="Выберете предложенные года, за которые вы хотите увидеть статистику:",
            reply_markup=get_keyboard4()
        )

    elif data == CALLBACK_BUTTON7_COAL_16:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2016 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} составляет:\n{res}',
        )
    elif data == CALLBACK_BUTTON8_COAL_15:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2016 год\n" + ex[1] + " млн тн за 2015 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} составляет:\n{res}',
        )
    elif data == CALLBACK_BUTTON9_COAL_14:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2016 год\n" + ex[1] + " млн тн за 2015 год\n" + ex[2] + " млн тн за 2014 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} составляет:\n{res}',
        )
    elif data == CALLBACK_BUTTON10_COAL_13:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2016 год\n" + ex[1] + " млн тн за 2015 год\n" + ex[2] + " млн тн за 2014 год\n" + ex[3] + " млн тн за 2013 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} составляет:\n{res}',
        )


    elif data == CALLBACK_BUTTON11_CO2_18:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2018 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} составляет:\n{res}',
        )

    elif data == CALLBACK_BUTTON12_CO2_14:

        ex = information[type][countryid]
        res = ex[0] + " млн тн за 2018 год\n" + ex[1] + " млн тн за 2014 год\n"

        query.edit_message_text(
            text=current_text,
        )
        bot.send_message(
            chat_id=chat_id,
            text=f'{typen} в стране {country} состовляет:\n{res}',
        )






def message_handler(bot: Bot, update: Update):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'Пользователь'

    reply_text = f'Доброго времени суток, {name}.\nВас приветствует команда ecoStats!\nС помощью этого телеграм-бота вы сможете просматривать статистику крупнейших 4 стран.\nВыберете страну, чью информацию хотите просмотреть:'

    bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=reply_text,
        reply_markup=get_keyboard1(),
    )

def main():
    print('start')
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    handler = MessageHandler(Filters.all, message_handler)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)

    updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
