license = """github bot, a telegram bot to search in github!
Copyright (C) 2023  Mr. X, https://t.me/linux_nerd
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
print(license)
import requests
import telebot, os
import brod
from telebot import types

owner="6524015514"
token = os.getenv("TOKEN")
githubToken = os.getenv("GHTOKEN")
bot = telebot.TeleBot(
    token,
    disable_web_page_preview=True,
    parse_mode="Markdown",
    num_threads=50,
    )
devUrl = types.InlineKeyboardButton(text="Mr. X - المطور",  url="https://t.me/linux_nerd")
foss = "This bot is foss, you can find the source code on https://github.com/n30mrx/githubot"

def brodD(msg):
    ids = open('ids.txt','r').readlines()
    brod.Brod(
        bot=bot,
        ids=ids,
        message=msg,
    )

@bot.message_handler(commands=['start'])
def start(message):
    with open('ids.txt','r') as f:
        if not str(message.chat.id)in f.read():
            with open('ids.txt','a') as ff:
                ff.write(f"\n{message.chat.id}")
    myKey  = types.InlineKeyboardMarkup(row_width=3)
    useBot = types.InlineKeyboardButton(text="استعمال البوت - use the bot", switch_inline_query_current_chat="")
    myKey.add(devUrl)
    myKey.add(useBot)
    bot.send_message(message.chat.id,"Hey! this is an inline bot used to search through [Github](https://github.com) :)\njust mention the bot and type your query, then choose a result!", reply_markup=myKey)
    if str(message.from_user.id)==owner:
        bot.send_message(
            chat_id=owner,
            text=f"Hello owner, The bot currently has {len(open('ids.txt','r').readlines())} users!"
        )
@bot.message_handler(commands=['brod'], func=lambda msg:str(msg.from_user.id)==owner)
def brodcast(msg):
    a =bot.send_message(
        msg.chat.id,
        "Send me a message and I will brodcast it"
    )
    bot.register_next_step_handler(
        message=a,
        callback=brodD
    )

@bot.message_handler(commands=["send"], func=lambda msg:str(msg.from_user.id)==owner)
def sendStorage(msg):
    bot.send_document(
        chat_id=msg.chat.id,
        document=open("ids.txt","rb")
    )

@bot.inline_handler(func=lambda query: len(query.query)>0)
def inline(inlineQuery):
    req = requests.get(
        headers={
            "Authorization":githubToken,
            "X-GitHub-Api-Version": "2022-11-28"
        },
        url=f"https://api.github.com/search/repositories?q={inlineQuery.query}&sort=stars&order=desc&per_page=50"
    )
    reqJ = req.json()['items']
    c = 0
    results = []
    for i in reqJ:
        resultsT = i['name']
        # resultsT = str(resultsT).replace(".","\\.")
        # resultsT = str(resultsT).replace("-","\\-")
        print(f"\n==================\n{resultsT}")
        resultsL = i['html_url']
        # resultsL = str(resultsL).replace(".","\\.")
        # resultsL = str(resultsL).replace("-","\\-")
        print(f"\n==================\n{resultsL}")
        resultsD=i['description']
        # resultsD = str(resultsD).replace(".","\\.")
        # resultsD = str(resultsD).replace("-","\\-")
        print(f"\n==================\n{resultsD}")

        resultsO = i['owner']
        Oname = str(resultsO['login']).replace('-','\\-')
        Ourl = str(resultsO['html_url']).replace('-','\\-')


        resultsM =f"Check [{resultsT}]({resultsL}) by [{Oname}]({Ourl}) \n{i['stargazers_count']}⭐️  {i['forks']}🍴:\n\n{resultsD}"
        results.append(types.InlineQueryResultArticle(id=c, title=resultsT, input_message_content=types.InputTextMessageContent(disable_web_page_preview=False, message_text=resultsM,parse_mode="Markdown"),description=resultsD,url=resultsL,thumbnail_url=resultsL))
        print(f"\n==================\nappended {resultsT}: {resultsL}")
        c+=1
    bot.answer_inline_query(inlineQuery.id,results=results)
    print(f"query {inlineQuery.id} answered!")


@bot.inline_handler(func=lambda query: len(query.query)==0)
def empty_inline(inlineQuery):
    results  = [
        types.InlineQueryResultArticle(id="dev",  title="Mr. X - المطور", url="https://t.me/linux_nerd",  input_message_content=types.InputTextMessageContent(message_text=license), hide_url=False),
        types.InlineQueryResultArticle(id="source",  title="Source code on github", url="https://github.com/n30mrx/archwikibot",  input_message_content=types.InputTextMessageContent(message_text=f"{foss}\n{license}"),description=foss),
    ]
    bot.answer_inline_query(inlineQuery.id, results=results)


bot.infinity_polling()
