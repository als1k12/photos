import time, threading, schedule, telebot, random
from telebot import TeleBot
import images_memes
import images_nomemes

token = "это мой токен"
bot = telebot.TeleBot("тут тоже")


mem_images = ['images_memes/kot.jpg' , 'images_memes/ded.jpg' , 'images_memes/monkey.jpg']
nomemes_images = ['images_nomemes/kot.jpg' , 'images_nomemes/kot2.jpg' , 'images_nomemes/kot3.jpg']


@bot.message_handler(commands=['mem'])
def send_mem(message):
     img = random.choice(mem_images)
     with open(img, 'rb') as f:
        bot.send_photo(message.chat.id, f)


@bot.message_handler(commands=['photo'])
def send_photo(message):
     img2 = random.choice(nomemes_images)
     with open(img2, 'rb') as f:
        bot.send_photo(message.chat.id, f)

print("Бот запущен.")
bot.polling()
