from slacker import Slacker
from config import config

API_KEY = config['slack']['API_KEY']
CHANNEL = config['slack']['CHANNEL']
slacker = Slacker(API_KEY)


def post(_str, pretext=None, title=None, color="good", channel=None):
    if channel is None:
        channel = CHANNEL
    slacker.chat.post_message(channel,
                              as_user=True,
                              attachments=[
                                  {
                                      "title": title,
                                      "pretext": pretext,
                                      "color": color,
                                      "text": _str
                                  }
                              ]
                              )


def ppost(_str, pretext=None, title=None, color="good", channel=None):
    print(_str)
    post(_str, pretext, title, color, channel)


def show_help():
    info = """
簡単にslackに通知するもの。
takagiken の wsl-bot を使います。

post:
   postでメッセージを送れます。
   必須は枠内のテキスト
   以下はoptional
   pretextは枠外のテキスト
   titleは枠内太字のテキスト
   colorは枠の色。danger, good, warningなど。デフォルト good（緑）
   channelはチャンネル名。デフォルト syunyooo-bot-notify
   channelでは、wsl-botを招待しておく必要があります。

ppost:
   基本postと同じ。同時にprintします。

"""
    print(info)
