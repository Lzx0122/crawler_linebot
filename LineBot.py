from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random


# 呼叫爬蟲
from crawler_104 import get_104

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')


line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):

    msg = get_msg(event.message.text)

    try:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    except Exception as e:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=e)
        )


def get_msg(input):
    if input == "資訊":
        msg = get_104()

        return msg
    if input == "指令":
        msg = "104找工作：\n104 <搜尋關鍵字> <地區>,<地區> <尋找頁數>"

        return msg
    inputlist = input.split(' ')
    if inputlist[0] == "104":
        if(len(inputlist) != 4):
            msg = "你的指令格式輸入錯誤"

            return msg
        return get_104(inputlist)


if __name__ == "__main__":
    app.run()
