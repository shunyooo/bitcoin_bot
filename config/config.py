import argparse
import configparser
CONFIG_PATH = 'config/config.ini'
config = configparser.ConfigParser()


def read_config(path=None):
    global CONFIG_PATH
    if path is not None:
        CONFIG_PATH = path
    print("config 読み込み -> {}".format(CONFIG_PATH))
    config.read(CONFIG_PATH)
    return config

read_config()
