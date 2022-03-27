from Assistant import Assistant
from provider import PriceProvider

from flask import Flask, request, abort
import os

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

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "crypto root"


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    receive_message = event.message.text
    crypto_list = ['BTC', 'ETH']
    currency_list = ['USD', 'JPY']

    if receive_message.isalpha() and receive_message.upper() == 'HELP':
        text_list = ['0:BTC 1:ETH ',
                     '0:USD 1:JPY ']
        assistant = Assistant()
        reply_message = assistant.get_help_message(text_list)
    else:
        try:
            crypto_index = int(receive_message[0])
            currency_index = int(receive_message[-1])
        except Exception as e:
            # error
            print(e)

        if len(crypto_list) >= crypto_index and \
                len(currency_list) >= currency_index:
            price_provider = PriceProvider()
            time = price_provider.get_request_time()
            crypto_name = crypto_list[crypto_index]
            currency_name = currency_list[currency_index]
            price = price_provider.get_price(crypto_name, currency_name)
            url = price_provider.url
            reply_message = f'{time}\r\n{crypto_name}:{price} {currency_name}\r\n{url}'
            print(reply_message)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    #    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
