import telebot
import random
import flob

API_TOKEN = '7789092398:AAFP5XpljnvqJwFds3UiO3wbfxsUTeiUUog'  # Замените на ваш токен

bot = telebot.TeleBot(API_TOKEN)
b = None
flag = None
idtgreg = ''
import importlib
import flobtg


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global b
    global flag
    username = message.from_user.username
    print(username)

    flag = True
    if b is not None:
        with open('flobtg.py', 'w') as file:
            file.write(f"tgidcode = '{b}'\n")
        importlib.reload(flobtg)
        print(flob.tgidinentent)
        a = f'Ваш код: {b}'
        if username == idtgreg[1::] or username == flob.tgidinentent[1::]:
            bot.reply_to(message, a)
    else:
        print(flob.tgidinentent)
        b = random.randint(100000, 999999)
        with open('flobtg.py', 'w') as file:
            file.write(f"tgidcode = '{b}'\n")
        importlib.reload(flobtg)
        a = f'Ваш код: {b}'
        if username == idtgreg[1::] or username == flob.tgidinentent[1::]:
            bot.reply_to(message, a)


@bot.message_handler(func=lambda message: True)
def send_user_name(message):
    global b
    print(flob.tgidinentent)
    username = message.from_user.username
    if flag:  # Username (никнейм), если есть
        a = f'Ваш код: {b}'
        with open('flobtg.py', 'w') as file:
            file.write(f"tgidcode = '{b}'\n")
        importlib.reload(flobtg)
        if username == idtgreg[1::] or username == flob.tgidinentent[1::]:
            bot.reply_to(message, a)
    else:
        b = random.randint(100000, 999999)
        with open('flobtg.py', 'w') as file:
            file.write(f"tgidcode = '{b}'\n")
        importlib.reload(flobtg)
        a = f'Ваш код: {b}'
        if username == idtgreg[1::] or username == flob.tgidinentent[1::]:
            bot.reply_to(message, a)


if __name__ == '__main__':
    print("Бот запущен.")
    bot.polling()
