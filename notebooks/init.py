# おまじない : パスの追加
import os
import sys
path = os.path.join(os.path.abspath(os.curdir), '../')
sys.path.append(path)

from config.config import read_config
config = read_config('../config/config.ini')
