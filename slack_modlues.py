# -*- coding: utf-8 -*-

import os
import sys
from slacker import Slacker

# get api token from your environment variable
slack_api_token = os.getenv("SLACK_API_TOKEN", None)
slack_debug_channel_id = os.getenv("SLACK_DEBUG_CHANNEL_ID", None)
slack_default_channel_id = os.getenv("SLACK_DEFAULT_CHANNEL_ID", None)
if slack_api_token is None:
    print("Specify SLACK_API_TOKEN as environment variable.")
    sys.exit(1)
if slack_debug_channel_id is None:
    print("Specify SLACK_DEBUG_CHANNEL_ID as environment variable.")
    sys.exit(1)
if slack_default_channel_id is None:
    print("Specify SLACK_DEFAULT_CHANNEL_ID as environment variable.")
    sys.exit(1)

slack = Slacker(slack_api_token)


def share_line_msg(msg):

    slack.chat.post_message(
        slack_debug_channel_id,
        text=msg,
        as_user=True
    )


def debug_line_msg(msg):

    slack.chat.post_message(
        slack_default_channel_id,
        text=msg,
        as_user=True
    )


if __name__ == '__main__':

    slack.chat.post_message(
        slack_debug_channel_id,
        'こんにちわー',
        as_user=True
    )
