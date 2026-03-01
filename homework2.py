import threading
from telebot import TeleBot

API_TOKEN = "8263397450:AAEG9A_UUCijklkBJLFnvJQ6lA2kdgbtgO4"
bot = TeleBot(API_TOKEN)

timers = {}


def beep(chat_id):
    bot.send_message(chat_id, "Beep!")
    if chat_id in timers:
        sec = timers[chat_id]["sec"]
        t = threading.Timer(sec, beep, args=[chat_id])
        timers[chat_id]["timer"] = t
        t.start()

@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.reply_to(message, "Команды:\n/set <сек>\n/unset")

@bot.message_handler(commands=["set"])
def set_timer(message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "Использование: /set <секунды>")
        return

    sec = int(args[1])
    if sec <= 0:
        bot.reply_to(message, "Введи число > 0")
        return

    chat_id = message.chat.id

    if chat_id in timers:
        timers[chat_id]["timer"].cancel()

    t = threading.Timer(sec, beep, args=[chat_id])
    timers[chat_id] = {"timer": t, "sec": sec}
    t.start()

    bot.reply_to(message, "Таймер каждые {sec} секунд запущен")

@bot.message_handler(commands=["unset"])
def unset_timer(message):
    chat_id = message.chat.id
    if chat_id in timers:
        timers[chat_id]["timer"].cancel()
        del timers[chat_id]
        bot.reply_to(message, "Таймер остановлен")
    else:
        bot.reply_to(message, "Нет активных таймеров")

print("Бот запущен")
bot.infinity_polling()

----------------------------------------------

import time, threading, schedule, telebot
from telebot import TeleBot
from logic import flip_coin, gen_emodji
import pass_generator
import test


token = "8263397450:AAEG9A_UUCijklkBJLFnvJQ6lA2kdgbtgO4"
bot = telebot.TeleBot("8263397450:AAEG9A_UUCijklkBJLFnvJQ6lA2kdgbtgO4")

images = ['shrek.png']

    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")
    
@bot.message_handler(commands=['hello'])
def send_hello(message):
        bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1:
        if args[1].isdigit():
            sec = int(args[1])
            if sec > 0:
                schedule.every(sec).seconds.do('beep', message.chat.id).tag(message.chat.id)
                bot.reply_to(message, f"Timer set for {sec} seconds!")
            else:
                bot.reply_to(message, 'Please enter a positive number of seconds.')
        else:
            bot.reply_to(message, 'Usage: /set <seconds> (seconds should be a number)')
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['luck'])
def send_luck(message):
     bot.reply_to(message, "Желаю тебе удачи на весь день!")

@bot.message_handler(commands=['photo'])
def send_photo(message):
     with open('images/shrek.png', 'rb') as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['store'])
def send_store(message):
     bot.reply_to(message, "Пока в ассортименте ничего нету. Возвращайся позже!")

@bot.message_handler(commands=['discord'])
def send_discord(message):
     bot.reply_to(message, "Скоро тут появится ссылка на дискорд, но пока нету..")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.reply_to(message, "Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.reply_to(message, "Монетка выпала так: {coin}")


@bot.message_handler(commands=['bot'])
def send_bot(message):
     bot.reply_to(message, "Бот создан с помощью @BotFather")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    bot.reply_to(message, pass_generator.password())
    
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


print("Бот запущен.") 
# bot.polling()

if __name__ == '__main__':
    threading.Thread(target=bot.polling, name='bot_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
