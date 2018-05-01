import os
import smtplib
# import configparser
from email.mime.text import MIMEText
from email.utils import formatdate
import message_texts
from debuger import send_debug_message

# get channel_secret and channel_access_token from your environment variable
from_address = os.getenv("FROM_ADDRESS", None)
from_passwd = os.getenv("FROM_PASSWORD", None)
to_address = os.getenv("TO_ADDRESS", None)
bcc_address = os.getenv("BCC_ADDRESS", None)

# get channel_secret and channel_access_token from ini file
# ini_file = configparser.ConfigParser()
# ini_file.read_file(open(file="config.ini"))
# from_address = ini_file.get("email", "FROM_ADDRESS")
# from_passwd = ini_file.get("email", "FROM_PASSWORD")
# to_address = ini_file.get("email", "TO_ADDRESS")
# bcc_address = ini_file.get("email", "BCC_ADDRESS")

# check
if from_address is None:
    print("Specify FROM_ADDRESS")
if from_passwd is None:
    print("Specify FROM_PASSWORD")
if to_address is None:
    print("Specify TO_ADDRESS")


def create_message(user_name, msg):

    email_msg = MIMEText(
        message_texts.create_email_message(
            user_name=user_name,
            msg=msg
        )
    )
    email_msg['Subject'] = message_texts.email_subject
    email_msg['From'] = from_address
    email_msg['To'] = to_address

    if bcc_address:
        email_msg['Bcc'] = bcc_address

    email_msg['Date'] = formatdate()

    return email_msg


def send(user_name, msg):

    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    try:
        smtpobj.login(
            from_address,
            from_passwd
        )
    except smtplib.SMTPAuthenticationError as e:
        send_debug_message(
            body=message_texts.debug_email_err + str(e)
        )
        return message_texts.email_err
    smtpobj.sendmail(
        from_address,
        to_address,
        create_message(
            user_name=user_name,
            msg=msg
        ).as_string())
    smtpobj.close()

    return message_texts.email_send_message


if __name__ == '__main__':

    print(send(user_name="テスト", msg="テスト"))
