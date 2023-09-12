FROM python:3.11

WORKDIR /app

# 更新套件庫並安裝依賴
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxss1 \
    libappindicator1 \
    tor

# 下載並安裝 Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome*.deb || apt-get install -f -y && \
    rm google-chrome-stable_current_amd64.deb

# 複製應用程式檔案
COPY . .
COPY ./torrc /etc/tor/torrc

# 安裝Python依賴
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數 CRAWLER_START_TIME
ENV CRAWLER_START_TIME="00:00:00"

VOLUME [ "/app/log" ]

# 啟動應用程式
CMD ["/app/start.sh"]