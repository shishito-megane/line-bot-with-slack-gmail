import os
import sys
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
import message_parser
import message_texts

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
# developer_line_id = os.getenv("DEVELOPER_LINE_ID", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
# if developer_line_id is None:
#     print("Specify DEVELOPER_LINE_ID as environment variable.")

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


def send_debug_message(body):

    # # メッセージを開発者に伝える
    # line_bot_api.push_message(
    #     to=developer_line_id,
    #     messages=TextSendMessage(
    #         text=body
    #     )
    # )
    print(body)


def get_user_name(event):

    profile = line_bot_api.get_profile(event.source.user_id)

    return profile.display_name


def send_follow_message(event, user_name):

    follow_massage = message_texts.followd_message

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=follow_massage)
    )

    send_debug_message(
        body=message_texts.create_debug_followed_message(
            user_name=user_name
        )
    )


def send_unfollow_message():

    send_debug_message(
        body=message_texts.debug_unfollow_message
    )


def send_join_message(event):

    # 参加したグループのIDを取得
    group_id = event.source.group_id

    join_message = message_texts.join_message

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=join_message)
    )

    line_bot_api.push_message(
        to=group_id,
        messages=TextSendMessage(
            text="#使い方"
        )
    )

    # 参加中のgroup_idを更新
    values.update(group_id=group_id)

    send_debug_message(
        body=message_texts.debug_join_message
    )


def send_leave_message_and_leave(event):

    # 退出するグループのIDを取得
    group_id = event.source.group_id

    leave_message_previous = message_texts.leave_message

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
    finally:
        send_debug_message(
            body=message_texts.debug_leave_message
        )


def send_reply_group_message(event, user_name):

    # 参加中のgroup_idを念の為更新
    values.update(group_id=event.source.group_id)

    debug_msg = message_texts.create_debug_line_message(
        user_name=user_name,
        msg=event.message.text,
        talk_type="group"
    )

    # 送られたメッセージを調べる
    msg, flg = message_parser.parse_group_msg(
        message=event.message.text
    )

    # help
    if flg == "---h":
        line_bot_api.push_message(
            to=event.source.group_id,
            messages=TextSendMessage(
                text=message_texts.help_text
            )
        )
        debug_msg += message_texts.create_debug_command_message(
            command="---h"
        )

    # leave
    elif flg == "---l":
        send_leave_message_and_leave(event)
        debug_msg += msg

    # 開発者宛メッセージ
    elif flg == "----":
        debug_msg += message_texts.create_debug_command_message(
            command="----"
        )

    else:
        print("unknown message")

    # 開発者に送信
    send_debug_message(
        body=debug_msg
    )


def send_reply_room_message(event, user_name):

    send_debug_message(
        body=message_texts.create_debug_line_message(
            user_name=user_name,
            msg=event.message.text,
            talk_type="room",
        )
    )


def send_reply_user_message(event, user_name):

    received_msg = message_texts.info_received_message

    debug_msg = message_texts.create_debug_line_message(
        user_name=user_name,
        msg=event.message.text,
        talk_type="user"
    )

    # 送られたメッセージを調べる
    msg, flg = message_parser.parse_user_msg(
        message=event.message.text
    )

    # グループLINEに転送
    if flg == "l---":
        try:
            line_bot_api.push_message(
                to=values.now_group_id,
                messages=TextSendMessage(
                    text=message_texts.create_line_message(
                        user_name=user_name,
                        msg=msg
                    )
                )
            )
        except LineBotApiError as e:
            # サーバーの再起動時にメッセージの送り先が更新されてなかった場合
            received_msg += message_texts.send_group_unknown_message
            debug_msg += message_texts.debug_send_group_unknown_message
            debug_msg += e
        else:
            received_msg += message_texts.info_message_shered
        finally:
            debug_msg += message_texts.create_debug_command_message(
                command="l---"
            )

    # グループLINEとslackに転送
    elif flg == "ls--":
        print("実装中")
        try:
            line_bot_api.push_message(
                to=values.now_group_id,
                messages=TextSendMessage(
                    text=message_texts.create_line_message(
                        user_name=user_name,
                        msg=msg
                    )
                )
            )
            # todo: ここにslack転送メッセージをつける
        except LineBotApiError as e:
            # サーバーの再起動時にメッセージの送り先が更新されてなかった場合
            received_msg += message_texts.send_group_unknown_message
            debug_msg += message_texts.debug_send_group_unknown_message
            debug_msg += e
        else:
            received_msg += message_texts.info_message_shered
        finally:
            debug_msg += message_texts.create_debug_command_message(
                command="ls--"
            )

    # グループLINEとslacｋとgmailに転送
    elif flg == "lsg-":
        print("実装中")
        try:
            line_bot_api.push_message(
                to=values.now_group_id,
                messages=TextSendMessage(
                    text=message_texts.create_line_message(
                        user_name=user_name,
                        msg=msg
                    )
                )
            )
            # todo: ここにslack&gmail転送メッセージをつける
        except LineBotApiError as e:
            # サーバーの再起動時にメッセージの送り先が更新されてなかった場合
            received_msg += message_texts.send_group_unknown_message
            debug_msg += message_texts.debug_send_group_unknown_message
            debug_msg += str(e)
        else:
            received_msg += message_texts.info_message_shered
        finally:
            debug_msg += message_texts.create_debug_command_message(
                command="lsg-"
            )

    # help
    elif flg == "---h":
        received_msg = message_texts.help_text
        debug_msg += message_texts.create_debug_command_message(
            command="---h"
        )

    # leave ここでは使えない
    elif flg == "---l":
        received_msg += message_texts.unknown_command_message
        debug_msg += message_texts.create_debug_command_message(
            command="---l"
        )

    # 開発者宛メッセージ
    elif flg == "----":
        debug_msg += message_texts.create_debug_command_message(
            command="----"
        )

    else:
        print("unknown message")

    # メッセージを受け取ったことを本人に返信する
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=received_msg)
    )

    # 開発者にも伝える
    send_debug_message(
        body=debug_msg
    )
