
import re


def parse_user_msg(message):

    # help & leave
    help_flg = re.fullmatch(r"#使い方", message)
    leave_flg = re.fullmatch(r"#退出", message)

    # to line message
    l_msg = re.search(r"#--(.*)--#", message)

    # line + slack message
    ls_msg = re.search(r"##-(.*)-##", message)

    # line + slack + gmail message
    lsg_msg = re.search(r"###(.*)###", message)

    if help_flg:
        return None, "---h"
    elif leave_flg:
        return None, "---l"
    elif l_msg:
        return l_msg.group(1), "l---"
    elif ls_msg:
        return ls_msg.group(1), "ls--"
    elif lsg_msg:
        return lsg_msg.group(1), "lsg-"
    else:
        return message, "----"


def parse_group_msg(message):

    # help & leave
    help_flg = re.fullmatch(r"#使い方", message)
    leave_flg = re.fullmatch(r"#退出", message)

    if help_flg:
        return None, "---h"
    elif leave_flg:
        return None, "---l"
    else:
        return message, "----"


if __name__ == "__main__":

    print(parse_user_msg(message="#--グループラインにのせるのね--#"))
    print(parse_user_msg(message="##-slackにも流しちゃうぞ-##"))
    print(parse_user_msg(message="###メールもしちゃうぞ###"))

    print(parse_user_msg(message="#--グループラインにのせるのね--#ああ-##"))
    print(parse_user_msg(message="##-slackに##--も流しちゃうぞ-##"))
    print(parse_user_msg(message="###メールもしちゃうぞ###"))

    print(parse_user_msg(message="#使い方"))

    print(parse_user_msg(message="使い方"))
