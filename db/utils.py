from config import config
from sqlalchemy import create_engine, MetaData

url = '{dbms}://{user}:{pass}@{host}:{port}/{db}'.format(**config["db"])
engine = create_engine(url, echo=True)
