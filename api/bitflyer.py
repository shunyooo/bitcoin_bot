from config import config
import pybitflyer
bf_con = config["bitflyer"]
bitflyer = pybitflyer.API(
    api_key=bf_con["API_KEY"], api_secret=bf_con["SECRET_KEY"])
