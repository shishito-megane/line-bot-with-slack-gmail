help_text_user = """
こんなふうにしてね！

<<ボクとの個人トーク>>
ボタンを押すとその内容に応じてメッセージを転送するよ！
ボタン以外の会話はslackを経由してボクを作ってくれた人に届けるんだ．

<<コマンド>>
3分タイマーをセットしたいときは「#タイマー」と言ってください．
使い方を知りたいときは「#使い方」と言ってください．
"""

help_text_group = """
こんなふうにしてね！

<<ボクとのグループトーク>>
ボクは個人トークからお知らせしてもらった内容を転送するよ！
新しいグループから招待されると，参加していたグループからはサヨナラするんだ．

<<コマンド>>
3分タイマーをセットしたいときは「#タイマー」と言ってください．
使い方を知りたいときは「#使い方」と言ってください．
グループから席を外して欲しいときは「#退出」と言ってください．

<<技術的な詳細>>
https://github.com/shishito-megane/line-bot-with-slack-gmail/
"""


followd_message = """
友達追加ありがとうございます\uDBC0\uDC78
どうぞよろしくお願いします\uDBC0\uDCB3
"""

join_message = """
はじめまして\uDBC0\uDC8A
ボクは大学1年生の「ケンタ」って言います．
センパイからの伝言を伝えます．
友達に追加してないセンパイは追加してね\uDBC0\uDCB3
使い方を知りたいときは次のように言ってみてね．
"""

leave_message = """
ボクは去ります...\uD8C0\uDC7C
いままで仲良くしてくれてありがとう！！
これからも個人トークで仲良くしてね！
"""

timer_set_message = "タイマーをセットしました．3分後にお知らせするよ！"

timer_complete_message = """3分経ちました．カップ麺食べたいなー！"""

info_received_message = "メッセージを受け取りました．"

info_message_shered = "ほかのみんなにも伝えたよ！"

unknown_command_message = "その操作はここでは使えないよ!"

send_group_unknown_message = """
送信先のグループがわかりませんでした．
送りたいグループで「#動け！」と言ってください．
"""

unknown_display_name = "ボクがわからないユーザー(友達になってよ...)"

email_subject = "出欠連絡ボットからの新しいメッセージです"

email_err = "メールが送れませんでした．ボクを作ってくれた人に連絡してください．"

email_send_message = "メールを送ったよ！"

def create_line_message(user_name, msg):
    return "「"+user_name+"」センパイから「"+msg+"」と連絡がありました．"


def create_slack_message(user_name, msg):
    return "「"+user_name+"」センパイから「"+msg+"」と連絡がありました．"


def create_email_message(user_name, msg):
    return "出欠連絡ボットです．\n「"+user_name+"」さんから「"+msg+"」と連絡がありました．"


debug_unfollow_message = "誰かがブロックしました．．."

debug_join_message = "新しいグループに参加しました．"

debug_leave_message = "グループから退出しました．"

debug_send_group_unknown_message = "送信先エラー"

debug_send_leave_message_err = "サヨナラメッセージが送れませんでした"

debug_parse_message_err = "パースに失敗したようです"

debug_email_err = "メールが送れませんでした．"

debug_email_send_message = "メールを送りました．"


def create_debug_followed_message(user_name):
    return "新規フォロー:「" + user_name + "」"


def create_debug_line_message(user_name, msg, talk_type):
    return "「"+user_name+"」から「"+msg+"」 talk_type:"+talk_type


def create_debug_command_message(command,):
    return " command:"+command

