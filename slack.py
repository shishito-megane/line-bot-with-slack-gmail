# -*- coding: utf-8 -*-

import os
import sys
from slacker import Slacker

# get api token from your environment variable
slack_api_token = os.getenv("SLACK_API_TOKEN", None)
# developer_line_id = os.getenv("DEVELOPER_LINE_ID", None)
if slack_api_token is None:
    print("Specify SLACK_API_TOKEN as environment variable.")
    sys.exit(1)

slack = Slacker(slack_api_token)


def share_line_msg(msg):

    slack.chat.post_message(
        "CAFLC21H9",
        text=msg,
        as_user=True
    )


if __name__ == '__main__':

    slack.chat.post_message(
        "U3D7R5WQ",
        'こんにちわー',
        as_user=True
    )
