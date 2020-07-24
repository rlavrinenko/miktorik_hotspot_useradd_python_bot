#!/usr/bin/python3
# -*- coding: utf-8 -*-
import config,os,telebot,routeros_api,random
from random import random, randrange, randint
from telegram.ext import CommandHandler
bot = telebot.TeleBot(config.token)
connection = routeros_api.RouterOsApiPool('IP', username='user', password='pass', plaintext_login=True )
api = connection.get_api()
@bot.message_handler(commands=["start"])
def send_welcome(message):
    first = message.from_user.first_name
    last = message.from_user.last_name
    userid = message.from_user.id
    usernam=message.from_user.username
    msg = bot.send_message(message.chat.id,'Вітаємо '+ str(first) +' '+ str(last) + '! напишіть бажаний login для wifi мережі')
    uw=open("/patch_to_scr/users/"+str(usernam), "w")
    uw.write(str(userid) +' '+str(usernam)+' '+str(first)+' '+str(last))
    uw.close()
    bot.register_next_step_handler(msg, login)
def login(message):
   lw = open("/patch_to_scr/txt/"+str(message.chat.id)+"login.txt", "w")
   lw.write(message.text)
   lw.close()
   serrchuser=api.get_resource('/ip/hotspot/user/')
   useransver=serrchuser.get(comment=message.text)
   if str(useransver) == '[]':
     msg = bot.send_message(message.chat.id, 'Бажаний пароль в мережі')
     bot.register_next_step_handler(msg, passw)
   else:
     msg = bot.send_message(message.chat.id, 'Вибачте: \nОбраний login: '+message.text+'\nВже зареєстровано \n Натисніть /start та вигадайте інший логін' )
     bot.register_next_step_handler(msg, send_welcome)
     print (useransver) 
def passw(message):
     pw = open("/patch_to_scr/txt/"+str(message.chat.id)+"pass.txt", "w")
     pw.write(message.text)
     pw.close()
     ch1=randint(1, 20)
     ch2=randint(1, 20)
     sum=ch1+ch2
     suw=open("/patch_to_scr/txt/"+str(message.chat.id)+"sum.txt", "w")
     suw.write(str(sum))
     suw.close()
     msg = bot.send_message(message.chat.id, 'Скільки буде '+str(ch1)+'+'+str(ch2)+'?')
     bot.register_next_step_handler(msg, capt)

def capt(message):
     sumendo=open("/patch_to_scr/txt/"+str(message.chat.id)+"sum.txt")
     sumend=sumendo.read()
     if message.text == str(sumend):
        log=open("/patch_to_scr/txt/"+str(message.chat.id)+'login.txt')
        login=log.read()
        pas=open("/patch_to_scr/txt/"+str(message.chat.id)+'pass.txt')
        passw=pas.read()
        idloginw=open("/patch_to_scr/idlogin/"+str(message.from_user.id), "w")
        idloginw.write(str(login))
        idloginw.close()
        hotspot_user= api.get_resource('/ip/hotspot/user/')
        hotspot_user.add(name=login,password=passw,comment=login,server="all",profile="authusers")
        msg = bot.send_message(message.chat.id, 'Дякуємо за реєстрацію, при наступному підключенні можете використовувати ваші данні \n Будемо вдячні за лайк, репост, chek-in нашої сторінки Facebook \n facebook.com')
     else:
         msg = bot.send_message(message.chat.id, 'Правильна відповідь:'+str(sumend)+'\nВаша відповідь не вірна. натисніть /start та повторіть реєстрацію')
@bot.message_handler(commands=["stat"])
def send_stat(message):
    logn=open("/patch_to_scr/idlogin/"+str(message.from_user.id))
    loginwifi=logn.read()
    msg = bot.send_message(message.chat.id,'Команда в розробці')
   # По этой команде подбираю реализацию статистики
if __name__ == '__main__':
    bot.polling(none_stop=True)
