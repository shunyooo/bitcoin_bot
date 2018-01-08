import argparse
import configparser
import subprocess
CONFIG_PATH = 'config/config.ini'
config = configparser.ConfigParser()


def change_db(section):
    if section in config.keys():
        config["db"] = config[section]
        print("changed db to {}".format(section))
    else:
        print("{} は {}内にはありません。".format(section, get_db_sections()))


def check_is_dead_db(quiet=True):
    # 死活監視のマシンのIPアドレス
    db_sections = get_db_sections()
    # マシンのIPアドレスを一つずつ取り出してpingコマンドを実行
    for sec in db_sections:
        _config = config[sec]
        host = _config["HOST"]
        print("section: {}".format(sec))
        ping(host, quiet)


def ping(host, quiet=True):
    loss_pat = '0 received'
    unknouwn_pat = 'Unknown host'
    msg_pat = 'icmp_seq=1 '
    ping = subprocess.Popen(
        ["ping", "-c", "1", host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = ping.communicate()
    msg = ''
    if unknouwn_pat in error.decode('utf-8'):
        msg = error.decode('utf-8').split("\n")[0]
        flag = False
    else:
        for line in out.splitlines():
            line = line.decode('utf-8')
            if not quiet:
                print(line)
            if msg_pat in line:
                msg = line.split(msg_pat)[1]  # エラーメッセージの抽出
            if loss_pat in line:  # パケット未到着ログの抽出
                flag = False
                break
        else:
            flag = True  # breakしなかった場合 = パケットは到着している

    if flag:
        print('[OK]: ' + 'ServerName->' + host)
    else:
        print('[NG]: ' + 'ServerName->' +
              host + ', Msg->\'' + msg + '\'')


def get_db_sections():
    return [sec for sec in config.keys() if "db" in sec]


def read_config(path=None):
    global CONFIG_PATH
    if path is not None:
        CONFIG_PATH = path
    print("config 読み込み -> {}".format(CONFIG_PATH))
    config.read(CONFIG_PATH)
    if "db_default" in config.keys():
        config["db"] = config["db_default"]
    return config

read_config()
