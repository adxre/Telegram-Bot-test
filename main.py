import telebot
from telebot import types
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

user_q_pos = {}
user_q_answers = {}

questions = pd.read_csv('questions3.csv')
questions_size = questions.shape[0]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для тестирования личности по методике Майерса-Бриггса. Для начала теста "
                          "введите команду /test. Для получения списка доступных команд введите /help.")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Помощи не будет.")


@bot.message_handler(commands=['test'])
def send_test(message):
    # сохраняем позицию вопроса
    user_q_pos[message.chat.id] = 0
    # сохраняем ответы которые получаем от пользователя
    user_q_answers[message.chat.id] = []

    # запускаем первый вопрос
    msg = bot.send_message(message.chat.id, questions.question[0])
    bot.register_next_step_handler(msg, process_answer)

    # q_str = str(questions.question[0])
    #
    # markup = InlineKeyboardMarkup()
    # markup.row_width = 2
    # markup.add(InlineKeyboardButton(q_str[q_str.index("а)"):q_str.index("б)")], callback_data="A"),
    #            InlineKeyboardButton(q_str[q_str.index("б)"):], callback_data="B"))
    #
    # msg = bot.send_message(message.chat.id, q_str[:q_str.index("а)")], reply_markup=markup)


def process_answer(message):
    if str(message.text).lower() not in 'абab':
        bot.send_message(message.chat.id, "Некорректный выбор ответа!")
        bot.register_next_step_handler(message, process_answer)
    else:
        user_q_pos[message.chat.id] = user_q_pos[message.chat.id] + 1
        user_q_answers[message.chat.id].append(message.text)

        if user_q_pos[message.chat.id] < questions_size:
            msg = bot.send_message(message.chat.id, questions.question[user_q_pos[message.chat.id]])
            bot.register_next_step_handler(msg, process_answer)
        else:

            score = []
            user_ie = 0
            user_sn = 0
            user_jp = 0
            user_tf = 0
            for answer in user_q_answers.values():
                score.append(answer)
            score1 = score[0]


            for i in range(0, len(score1), 7):
                if score1[i] in "aAАа":
                    user_ie += 1
            for i in range(1, len(score1), 7):
                if score1[i] in "aAАа":
                    user_sn += 1
            for i in range(2, len(score1), 7):
                if score1[i] in "aAАа":
                    user_sn += 1
            for i in range(3, len(score1), 7):
                if score1[i] in "aAАа":
                    user_tf += 1
            for i in range(4, len(score1), 7):
                if score1[i] in "aAАа":
                    user_tf += 1
            for i in range(5, len(score1), 7):
                if score1[i] in "aAАа":
                    user_jp += 1
            for i in range(6, len(score1), 7):
                if score1[i] in "aAАа":
                    user_jp += 1
            if user_ie > 5:
                user_i = 'E'
            else:
                user_i = 'I'
            if user_sn > 10:
                user_n = 'S'
            else:
                user_n = 'N'
            if user_tf > 10:
                user_f = 'T'
            else:
                user_f = 'F'
            if user_jp > 10:
                user_p = 'J'
            else:
                user_p = 'P'

            personality_type = user_i + user_n + user_f + user_p

            bot.send_message(message.chat.id, "Ваш тип личности: " + personality_type)

            user = message.from_user.username
            id = message.from_user.id
            file = open(str(id)+'.txt', 'w')
            # Записываем
            file.write("User: {}, id: {}, result: {},answes: {}\n".format(user, id, personality_type,str(user_q_answers[message.chat.id])))
            file.close()



            # ресет значений
            user_q_pos[message.chat.id] = 0
            user_q_answers[message.chat.id] = []


bot.infinity_polling()
