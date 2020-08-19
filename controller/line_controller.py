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

from utils.db import create_lottery, count_lottery

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
        user_id = event.source.user_id
        event_name = event.video_play_complete.tracking_id
        count = count_lottery()
        if count > 3:
            message = "可惜～下次手腳要快一點！"
        else:
            row = create_lottery(line_id=user_id, name=event_name)
            if row:
                message = "恭喜你中獎！找講者領禮物囉🎁"
            else:
                message = "你太貪心囉！"
        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage(text=message)]
        )

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        text = event.message.text
        if text == 'video':
            line_bot_api.reply_message(
                event.reply_token,
                messages=VideoSendMessage(
                    original_content_url='https://i.imgur.com/TJJYqmH.mp4',
                    preview_image_url='https://i.imgur.com/MW0Mpb6.jpg',
                    tracking_id='FRESH')
            )
