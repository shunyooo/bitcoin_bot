from slacker import Slacker
from .slack_post import modificate

API_KEY = ""
CHANNEL = "doj_python_alert"    # チャンネル名。事前にbotを招待しておく。
MODIFICATE_MODE = "code"        # コメント修飾の種類
POST_INTERVAL = 5               # editする間隔(%) 5%だと20回の更新が見込まれる。


class SlackProgress(object):
    """
    スラックにプログレスを通知するクラス。
    一つのメッセージを更新していくことによって、メッセージの氾濫を防ぐ。
    """

    def __init__(self, token=API_KEY, channel=CHANNEL, suffix='%'):

        self.suffix = suffix
        self.channel = channel
        self.slack = Slacker(token)

    def new(self, total=100, post_interval=POST_INTERVAL):
        """
        ProgressBarオブジェクトの生成、返却
        @param total(int): progressの最大値
        """
        res = self.slack.chat.post_message(
            self.channel, self._makebar(0), as_user=True)
        bar = ProgressBar(self, total, post_interval)
        bar.msg_ts = res.body['ts']
        bar.channel_id = res.body['channel']
        return bar

    def iter(self, iterable, fin_delete=True, bar_object=None):
        """
        iterableオブジェクトをラップし、自動でprogress barを作成。
        iterateする度にupdateする。
        @param iterable(iterable): for i in sp.iter(range(500))みたいな
        @param fin_delete: 終了時にメッセージを消すかどうか
        @param bar_object: 呼び出し先でbarを参照したい時に、ここに渡して参照を得る。
        """
        bar = self.new(total=len(iterable) - 1)
        bar_object = bar
        for idx, item in enumerate(iterable):
            yield(item)
            bar.done = idx
        if fin_delete:
            bar.delete()

    def _update(self, chan, msg_ts, pos, comment):
        print("[update slack message] pos:{}, comment:{}".format(pos, comment))
        self.slack.chat.update(chan, msg_ts, self._makebar(pos) + comment)

    def _makebar(self, pos):
        bar = (round(pos / 5) * chr(9608))
        return '{} {}{}'.format(bar, pos, self.suffix)

    def _delete(self, chan, msg_ts):
        self.slack.chat.delete(chan, msg_ts)


class ProgressBar(object):
    """
    プログレスバーの実体クラス。
    呼び出し側ではこのクラスに対してsetすることでslackのメッセージが更新される。
    """

    msg_ts = None     # メッセージのタイムスタンプ。一意にeditする。
    channel_id = None  # channelのid。

    def __init__(self, sp, total, post_interval):
        self._sp = sp
        self._pos = 0
        self._done = 0
        self._comment = ""
        self.total = total
        self.post_interval = post_interval
        self.force = False
        self.mode = "running"

    @property
    def done(self):
        """Get done. 絶対値を返す"""
        return self._done

    @done.setter
    def done(self, val):
        """Set done."""
        self._done = val
        self.pos = round((val / self.total) * 100)

    @property
    def pos(self):
        """Get pos. パーセンテージを返す"""
        return self._pos

    @pos.setter
    def pos(self, val):
        """Set pos. setされるとslackを更新"""
        if (val != self._pos and val - self._pos >= self.post_interval) or self.force:
            self._sp._update(self.channel_id, self.msg_ts, val, self.comment)
            self._pos = val
            self.force = False

    @property
    def comment(self):
        """Get comment. 付加的な文字列情報"""
        if self._comment == "":
            return self._comment
        else:
            return "\n" + modificate(self._comment, MODIFICATE_MODE)

    @comment.setter
    def comment(self, val):
        """Set comment."""
        self._comment = val
        self._sp._update(self.channel_id, self.msg_ts, self.pos, self.comment)

    def delete(self):
        self._sp._delete(self.channel_id, self.msg_ts)

    def set(self, __done, __comment="", force=False, mode="running"):
        """
        doneとcommentをそれぞれsetすると
        update が重複して呼び出されるので、両方とも変更する場合はこれ。
        """
        self.force = force
        self._comment = __comment
        self.done = __done
        self.mode = mode

    def __del__(self):
        if self.mode == "running":
            self.set(self.done, "running is stopped!!", True)
        elif self.mode == "done_delete":
            self.delete()
