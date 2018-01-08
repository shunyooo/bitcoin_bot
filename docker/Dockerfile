FROM ubuntu:16.04
MAINTAINER syunyooo

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
# Python3 と pip3, 日本語パッケージ
RUN apt-get update \
  && apt-get install -y python3 \
                        python3-pip \
                        language-pack-ja \
                        vim \
                        python-dev \
                        libmysqlclient-dev \
                        sudo \
                        mecab libmecab-dev mecab-ipadic \
                        mecab-ipadic-utf8 \
                        python-mecab \
                        git \
                        iputils-ping \
                        net-tools \
                        dnsutils

RUN apt-get install -y curl

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git\
    && cd mecab-ipadic-neologd\
    && bin/install-mecab-ipadic-neologd -n -y

# mysqlのinstall
# そのままapt-getでインストールするとパスワードを聞かれる箇所で止まってしまうので、予め設定しておく。この例ではパスワードは「root」。
RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections && \
    apt-get -y install mysql-server

# pip install
COPY requirements.txt /usr/src/app/
RUN pip3 install --upgrade pip \
    && pip3 install -r /usr/src/app/requirements.txt

# 日本語のフォントのインストール
RUN apt-get install -y fonts-migmix
# フォントの設定書き換え
COPY docker_local.conf /etc/fonts/local.conf

ENV LANG ja_JP.UTF-8
ENV PYTHONIOENCODING utf_8

# jupyterの設定
RUN jupyter notebook --generate-config
# jupyter extention系
RUN jupyter contrib nbextension install --user
RUN git clone https://github.com/ipython-contrib/IPython-notebook-extensions\
    && cd IPython-notebook-extensions\
    && sudo python3 setup.py install\
    && cd ../\
    && rm -rf IPython-notebook-extensions

# ローカル時間を東京に変更
# RUN echo "Asia/Tokyo" | tee /etc/timezone \
#    dpkg-reconfigure --frontend noninteractive tzdata
ENV TZ Asia/Tokyo

CMD ["/bin/bash"]