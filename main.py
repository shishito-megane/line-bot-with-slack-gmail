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
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
developer_line_id = os.getenv("DEVELOPER_LINE_ID", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
if developer_line_id is None:
    print("Specify DEVELOPER_LINE_ID as environment variable.")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


class Values(object):
    """現在参加中のgroup_idを保持"""

    def __init__(self, group_id):
        self.now_group_id = group_id

    def update(self, group_id):
        print(str(self.now_group_id)+" ->update-> "+str(group_id))
        self.now_group_id = group_id


# 初期値設定
values = Values(group_id="0")


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


def send_debug_message(body):

    # メッセージを開発者に伝える
    line_bot_api.push_message(
        to=developer_line_id,
        messages=TextSendMessage(
            text=body
        )
    )


def send_reply_user_message(event, profile):

    # メッセージを受け取ったことを本人に返信する
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="メッセージを受け取りました．")
    )

    send_debug_message(
        body="「" + profile.display_name + "」から個人トークで「" + event.message.text + "」"
    )


def send_reply_group_message(event, profile):

    # 参加中のgroup_idを念の為更新
    values.update(group_id=event.source.group_id)

    send_debug_message(
        body="「" + profile.display_name + "」からグループトークで「" + event.message.text + "」"
    )


def send_reply_room_message(event, profile):

    send_debug_message(
        body="「" + profile.display_name + "」からルームトークで「" + event.message.text + "」"
    )


@handler.add(MessageEvent, message=TextMessage)
def respond_reply_message(event):

    # for debug
    print(event)

    # 送信者のプロフィール取得
    profile = line_bot_api.get_profile(event.source.user_id)

    if event.source.type == "user":
        send_reply_user_message(event, profile)

    elif event.source.type == "group":
        send_reply_group_message(event, profile)

    elif event.source.type == "room":
        send_reply_room_message(event, profile)

    else:
        # ここに入ることはないハズ
        print("unknown type")


def send_followd_message(event, profile):

    follow_massage = """友達追加ありがとうございます\uDBC0\uDC78\nどうぞよろしくお願いします\uDBC0\uDCB3"""

    # 本人に返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=follow_massage)
    )

    send_debug_message(
        body="「" + profile.display_name + "」と友達になりました．"
    )


@handler.add(FollowEvent)
def respond_followed_message(event):

    # for debug
    print(event)

    # 送信者のプロフィール取得
    profile = line_bot_api.get_profile(event.source.user_id)

    send_followd_message(event, profile)


def send_unfollowd_message():

    send_debug_message(
        body="誰かがブロックしました．．"
    )


@handler.add(UnfollowEvent)
def send_unfollow_message(event):

    # for debug
    print(event)

    send_unfollowd_message()


def send_join_message(event, group_id):

    join_message = """はじめまして\uDBC0\uDC8A\nボクは大学1年生の「ケンタ」って言います\nセンパイからの伝言を伝えます\n友達に追加してないセンパイは追加してね\uDBC0\uDCB3\n使い方を知りたいときは次のように言ってみてね．"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=join_message)
    )

    line_bot_api.push_message(
        to=group_id,
        messages=TextSendMessage(
            text="**help"
        )
    )

    # 参加中のgroup_idを更新
    values.update(group_id=event.source.group_id)

    send_debug_message(
        body="新しいグループに参加しました．"
    )


def send_leave_message(event, group_id):

    leave_message_previous = """ボクは去ります...\uD8C0\uDC7C\nいままで仲良くしてくれてありがとう！！\nこれからも個人トークで仲良くしてね！"""

    try:
        line_bot_api.push_message(
            to=group_id,
            messages=TextSendMessage(
                text=leave_message_previous
            )
        )
    except LineBotApiError as e:
        print("サヨナラメッセージが送れませんでした")
        print(e)
    else:
        line_bot_api.leave_group(group_id=group_id)

    send_debug_message(
        body="グループから退出しました．"
    )


@handler.add(JoinEvent)
def respond_join_event(event):

    # for debug
    print(event)

    # 参加したグループのIDを取得
    group_id = event.source.group_id

    send_join_message(event, group_id)


@handler.add(LeaveEvent)
def respond_leave_event(event):

    # for debug
    print(event)

    # 退出したグループのIDをを取得
    group_id = event.source.group_id

    send_leave_message(event, group_id)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
