#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import os
import constant
import urllib.request as urllib2
import requests

bot = telebot.TeleBot(constant.token)

bot_data = bot.get_me()
print(" Bot_id: {0} \n Bot: {1} \n Bot name: {2}".format(
    str(bot_data.id),
    bot_data.username,
    bot_data.first_name
  ))

def log(message, answer):
  print("\n ========")
  from datetime import datetime
  print(datetime.now())
  print(" Message: from: {0} {1}, (id = {2}) \n Text: {3}".format(
      message.from_user.first_name,
      message.from_user.last_name,
      str(message.from_user.id),
      message.text
    ))
  print(" Answer: {0}".format(answer))

@bot.message_handler(commands=['start'])
def handle_command(message):
  user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
  user_markup.row('/stop', '/weather')
  bot.send_message(message.from_user.id, 'Welcome', reply_markup=user_markup)
  log(message, 'show keyboard for reply')

@bot.message_handler(commands=['stop'])
def handle_command(message):
  remove_markup = telebot.types.ReplyKeyboardRemove()
  bot.send_message(message.from_user.id, 'keyboard removed', reply_markup=remove_markup)
  log(message, 'keyboard removed')

@bot.message_handler(commands=['weather'])
def handle_command(message):
  markup = telebot.types.ForceReply(selective=False)
  bot.send_message(message.from_user.id, "Type city:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
  api_url = 'http://api.openweathermap.org/data/2.5/find'
  params = {
    'q' : message.text,
    'units' : 'metric',
    'APPID' : constant.app_id,
    'lang' : 'ru'
  }
  res = requests.get(api_url, params)
  res = res.json()
  answer = "Температура: {0}, \n Погода: {1}".format(
      res['list'][0]['main']['temp'],
      res['list'][0]['weather'][0]['description']
    )
  bot.send_message(message.from_user.id, answer)
  log(message, answer)

bot.polling(none_stop=True)