from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os

from Provider import PriceProvider
from Provider import option_list_with_index

app = Flask(__name__)


LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    crypto_list = ['BTC', 'ETH']
    currency_list = ['USD', 'JPY']
    for one_list in [crypto_list, currency_list]:
        option_list_with_index(one_list)
    receive_message = event.message.text
    # input_value = input('(i.e:01,10,11,00)\r\nPlease enter the number...')
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
        TextSendMessage(text=reply_message)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
