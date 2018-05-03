# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os

from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent
)
import line_modules

line_bot_api = line_modules.line_bot_api
handler = line_modules.handler


app = Flask(__name__)


# LINEからのイベントハンドラー
@app.route("/callback", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    print(request)

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def respond_reply_message(event):

    # for debug
    print(event)

    user_name = line_modules.get_user_name(event=event)

    if event.source.type == "user":
        line_modules.send_reply_user_message(
            event=event,
            user_name=user_name
        )

    elif event.source.type == "group":
        line_modules.send_reply_group_message(
            event=event,
            user_name=user_name
        )

    elif event.source.type == "room":
        line_modules.send_reply_room_message(
            event=event,
            user_name=user_name
        )

    else:
        # ここに入ることはないハズ
        print("unknown type")


@handler.add(FollowEvent)
def respond_followed_message(event):

    # for debug
    print(event)

    user_name = line_modules.get_user_name(event=event)

    line_modules.send_follow_message(
        event=event,
        user_name=user_name
    )


@handler.add(UnfollowEvent)
def send_unfollow_message(event):

    # for debug
    print(event)

    line_modules.send_unfollow_message()


@handler.add(JoinEvent)
def respond_join_event(event):

    # for debug
    print(event)

    line_modules.send_join_message(event=event)


@handler.add(LeaveEvent)
def respond_leave_event(event):

    # for debug
    print(event)

    line_modules.send_leave_message_and_leave(event=event)


if __name__ == "__main__":

    import debuger

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    debuger.send_debug_message(
        body="サーバーが再起動しました．"
    )
