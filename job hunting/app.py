import json
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage,
                            TemplateSendMessage, ButtonsTemplate, URITemplateAction, CarouselTemplate, CarouselColumn,
                            URIAction, FlexSendMessage, CameraAction, CameraRollAction, QuickReply,
                            QuickReplyButton, PostbackAction)
from linebot.exceptions import LineBotApiError

# 記得進去env.json裡面修改成自己要套用的LINE Bot API
with open('env.json') as f:
    env = json.load(f)

line_bot_api = LineBotApi(env['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(env['YOUR_CHANNEL_SECRET'])

app = Flask(__name__)

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
    except Exception as e:
        print("Error occurred while handling webhook: ", e)
        abort(500)

    return 'OK'


# 根據訊息內容做處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == '自我介紹':
        with open('intro.json', encoding='utf-8') as d:
            test1 = json.load(d)
        with open('intro_download.json', encoding='utf-8') as e:
            test2 = json.load(e)

        flex_message1 = FlexSendMessage('自我介紹', test1)
        flex_message2 = FlexSendMessage('資料下載', test2)

        line_bot_api.reply_message(
            event.reply_token, [flex_message1, flex_message2]
        )

    elif event.message.text == '作品集':
        with open('works.json', encoding='utf-8') as d:
            test = json.load(d)

        flex_message = FlexSendMessage('作品集', test)

        line_bot_api.reply_message(
            event.reply_token, flex_message
        )

    elif event.message.text == '聯絡資訊':
        with open('contact.json', encoding='utf-8') as d:
            test = json.load(d)

        flex_message = FlexSendMessage('聯絡資訊', test)

        line_bot_api.reply_message(
            event.reply_token, flex_message
        )


if __name__ == "__main__":
    app.run()
