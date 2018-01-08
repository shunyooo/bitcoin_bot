import db
import pandas as pd
from plotter.plot import plt, set_figure


class Simulator(object):
    """bitcoinのシミュレートを行うためのもの"""

    def __init__(self, start=None, end=None, sec_by=None):
        # データの取得
        self.ticker = db.df.read_ticker(start=start, end=end, sec_by=sec_by)
        print("data:{} - {}\nsamples:{}".format(self.ticker.index.min(),
                                                self.ticker.index.max(), self.ticker.shape[0]))
        self.action_space = ["buy", "sell", "stay"]

    @staticmethod
    def total_balance_yen(ltp, bitcoin, yen):
        return ltp * bitcoin + yen

    def simulate(self, agent, start_yen=None, show_plot=True):
        # agent は、ロジック関数 step を内包したクラス
        # step の引数はtimeとDataFrame（最新の1行）,
        # 返却は(買い buy、売り sell、何もしない stay), (量)の２つ

        # ログ用
        log = pd.DataFrame()

        def log_action(time, action, amount, bc, yen, total, **args):
            # time, action, amount, bc, yen, total
            nonlocal log
            #print("{time} {action} {amount}, bitcoin:{bc}, yen:{yen} total:{total}".format(time=time, action=action, amount=amount, bc=bc, yen=yen, total=total))
            info = pd.DataFrame({"action": [action], "amount": [amount], "bitcoin": [
                                bc], "yen": [yen], "total": [total], "total_ratio": [total / args['start_yen']]}, index=[time])
            log = log.append(info)

        balance_bitcoin = 0      # bitcoinの持っている量
        if start_yen is not None:
            balance_yen = start_yen  # 日本円の残高
        else:
            balance_yen = float(self.ticker.head(1).ltp)
        start_yen = balance_yen

        for time, row in self.ticker.iterrows():
            # 一行ずつデータを与えていく。
            action, amount = agent.step(time, row)
            # 何もしない
            if action == "stay":
                pass
            # 買い
            elif action == "buy":
                if balance_yen > row.ltp * amount:
                    balance_bitcoin += amount
                    balance_yen -= row.ltp * amount
                else:
                    # print("注文失敗 日本円残高:{} < 買い注文:{}".format(balance_yen, row.ltp*amount))
                    action = "buy failed"
            # 売り
            elif action == "sell":
                if balance_bitcoin > amount:
                    balance_bitcoin -= amount
                    balance_yen += row.ltp * amount
                else:
                    # print("注文失敗 　bitcoin残高:{} < 売り注文:{}".format(balance_bitcoin, amount))
                    action = "sell failed"
            log_action(time, action, amount, balance_bitcoin, balance_yen,
                       self.total_balance_yen(row.ltp, balance_bitcoin, balance_yen), start_yen=start_yen)

        print("simulate done. plot...")
        # 描画
        set_figure((16, 5))
        plt.plot(self.ticker[["ltp"]], label="ltp")
        # plt.legend()
        # plt.show()
        plt.plot(log[["total"]], label="total_balance", color="blue")
        plt.legend()
        if show_plot:
            plt.show()

        return log
