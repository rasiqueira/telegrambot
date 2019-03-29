# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 23:09:45 2019

@author: Rodrigo
"""

import telebot
import requests
import Algorithmia
import random
from instapy_cli import client


  
bot = telebot.TeleBot("758680216:AAHNhvUzg11w8J0a2iECb-WRCvp31yB-UcQ")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, u"Olá, bem-vindo ao Jiujitsu_figjters! Digite o nome do seu lutador preferido que vou postar sua foto no instagram https://www.instagram.com/jiujitsu_fighters/")
    
def listener(messages):
    for m in messages:
        
        print(m.text)
        cliente = Algorithmia.client('simtcMfVcIi2EcFstBQAJlyiiKe1')
        algo = cliente.algo('shashankgutha/WebsiteLinksRecommenderForkeywords/1.0.1')
        algo.set_options(timeout=300) # optional
        print (algo.pipe(m.text).result[0]['abstract'] + ' know more in '  + algo.pipe(m.text).result[0]['url'] )
        text = (algo.pipe(m.text).result[0]['abstract'] + ' know more in '  + algo.pipe(m.text).result[0]['url'])

        r = requests.get("https://api.qwant.com/api/search/images",
        params={
                'count': 50,
                'q': m.text,
                't': 'images',
                'safesearch': 1,
                'locale': 'en_US',
                'uiv': 4
                },
                headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                }
                )

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]
        print(random.choice(urls))
        
        
            
            

        input = {
                "image": random.choice(urls)
                }
        cliente = Algorithmia.client('simtcMfVcIi2EcFstBQAJlyiiKe1')
        algo = cliente.algo('util/SmartImageDownloader/0.2.18')
        algo.set_options(timeout=300) # optional
        save = algo.pipe(input).result
        save = save['savePath']
        localAbsPath = cliente.file(str(save[0])).getFile().name


        username = 'jiujitsu_fighters'
        password = 'rod@1220'
        image = localAbsPath
        text = text + "#jiujitsu #mma #legends #oss #gentleart"

        with client(username, password) as cli:
            cli.upload(image, text)
            




bot.set_update_listener(listener)

bot.polling()

