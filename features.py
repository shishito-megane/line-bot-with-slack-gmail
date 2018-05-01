import threading


def timer(sec, module):
    """指定時間後にモジュールを実行する"""

    t = threading.Timer(sec, module)
    t.start()
