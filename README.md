# bitcoin_bot
bitcoinの自動売買、データ取得などを行うbot。

docker図はまた書く。もし、本格的に利益が出るようになったらprivateにします。

jupyterでの開発、知見などは[./noteboks](notebooks)より。

# 実行、開発

1. bitflyerでAPIキーを取得。` config/config.ini ` でキーを設定。
2. ` docker-compose up ` 実行
   - appコンテナとdbコンテナが起動。
   - ホストのディレクトリがdockerにマウントされるので、開発が容易。
   - http://localhost:4444 で、jupyterでの開発が可能
   - DBはホストからアクセスする場合は、mysql://btc:bitcoin@localhost:3333/bitcoinから。
     dockerからアクセスする場合はmysql://btc:bitcoin@db:3306/bitcoinから。
   - 実行した段階で、自動でbitflyerからtickerをバッチで取得し、dockerのDBに突っ込んでいく。
3. ​



# 運用

1. どっかのサーバでssh,  `git clone`
2. `docker-compose up`
3. ファイアーウォールなど、3333, 4444ポートを解放しておく。
4. あとはコンソール切ってOK。ttyをFalseにしているので、バックグラウンドで回る。

## 他のDBサーバを使う場合
1. どっかのサーバでssh,  `git clone`
2. `config/config.ini`のdb設定を書き換え。
3. `docker-compose up app`
4. ファイアーウォールなど、4444ポートを解放しておく。
5. あとはコンソール切ってOK。ttyをFalseにしているので、バックグラウンドで回る。




# TODO

- slack 通知

  - データの容量がある程度増えたら
  - 売買の通知、戦略の通知
  - チャートの揺れ検知

- シミュレーションシステムの作成

  - ある戦略で行なった場合、〇〇の利益、その推移などグラフで出力できるように。

  - 時間ステップごとに行動を決定。それ以降で、その行動の評価を行うことができる。

    ​

