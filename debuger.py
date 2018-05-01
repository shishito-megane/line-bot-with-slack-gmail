
import line_modules
import slack_modlues

def send_debug_message(body):

    print(body)

    # # LINEで送る
    # line_bot_api.push_message(
    #     to=developer_line_id,
    #     messages=TextSendMessage(
    #         text=body
    #     )
    # )

    # slackで送る
    slack_modlues.debug_line_msg(
        msg=body
    )