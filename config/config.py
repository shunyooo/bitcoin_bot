import argparse
import configparser
CONFIG_PATH = 'config/config.ini'
print("config 読み込み -> {}".format(CONFIG_PATH))
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
