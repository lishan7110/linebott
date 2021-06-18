from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('VOgGjY7p6p41+zHZRYr31SMkDs/x3Z4Tx1OJkgS+r5vF2/NsVFAkNpm97YNbosQJXUdw1Lyt2Mwi8+ihg/7dSPcykQ5wxWZ9MFjo99BGj72ezjCxMiJwimJlpIBVKaNjqkL6lRVF8rxJtqUuysP3rAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d0b036db4600422c4b395c12dfb885c4')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()