import os
from flask import request
from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, VideoSendMessage, TextSendMessage)
from linebot.models.events import VideoPlayCompleteEvent

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


class LineIconSwitchController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(VideoPlayCompleteEvent)
    def handle_follow(event):
        print(event)
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(text="阿龜可愛ㄇ")
        )

    # do something
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        text = event.message.text
        user_id = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            messages=VideoSendMessage(
                original_content_url='https://i.imgur.com/1Os9Wz6.mp4',
                preview_image_url='https://stickershop.line-scdn.net/stickershop/v1/sticker/52002734/iPhone/sticker_key@2x.png',
                tracking_id="tttt")
        )
