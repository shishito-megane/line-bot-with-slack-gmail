import slack_modlues


def send_debug_message(body):

    print(body)

    # slackで送る
    slack_modlues.debug_line_msg(
        msg=body
    )
