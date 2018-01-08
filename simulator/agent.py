from abc import ABC
from abc import abstractmethod


class AgentInterface(ABC):
    """
    Simulator の simulateメソッド用のエージェントのインターフェイス。
    とりあえず step メソッドを実装せよ。
    """

    def __init__(self):
        super(AgentInterface, self).__init__()

    @abstractmethod
    def step(self, time, row_df):
        """
        Summary: データ取得毎にどう実行するかのロジックメソッド。
        Attributes: 
            @param (time): pd.Timestamp型のデータ取得日時
            @param (row_df): pd.Dataframe型のデータ本体。ticker。
        Returns: (買い "buy" 、売り "sell" 、何もしない "stay"):String, (量):floatの２つ
        """
        pass
