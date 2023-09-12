import random
from datetime import datetime, timedelta
import schedule
import threading
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from action import random_click, random_scroll, random_wait
from get_random import get_random_timestamp, get_random_array_element
from control_tor import renewTorNYM
from json_format import CustomJsonFormatter
from url import url_list

logger = logging.getLogger()

logHandler = logging.FileHandler("./log/log.txt")
formatter = CustomJsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Stream handler to display logs in the terminal
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.setLevel(logging.INFO)

def job(missionNumber):
    try:
        logger.info(f"第 {missionNumber} 個任務 - 任務開始 - {datetime.now()}")

        # 更新 Tor 的 NYM (與 IP 有關)
        logger.info(f"第 {missionNumber} 個任務 - Renew Tor NYM")
        renewTorNYM()

        # 設置 Chrome 以使用 Tor
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # 使用無痕模式
        chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
        chrome_options.add_argument("--headless")  # 啟用無頭模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 啟動 WebDriver
        driver = webdriver.Chrome(options=chrome_options)

        # 查詢我的IP位址
        driver.get("https://www.whatismyip.com.tw/tw/")

        ip = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-ip]'))
        )
        logger.info(f"第 {missionNumber} 個任務 - IP 位址 - {ip.text}")

        url = get_random_array_element(url_list)
        logger.info(f"第 {missionNumber} 個任務 - 預計訪問網站 - {url}")

        logger.info(f"第 {missionNumber} 個任務 - 開始訪問網站")
        driver.get(url)

        num_random_actions = random.randint(5, 15)
        logger.info(f"第 {missionNumber} 個任務 - 預計訪問 {num_random_actions} 次")
        for i in range(num_random_actions):
            logger.info(f"第 {missionNumber} 個任務 - 第 {i + 1} 次訪問該網站 - {url}")
            random_wait(1, 3)
            random_scroll(driver)
            random_wait(2, 6)
            random_click(driver)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            url = driver.current_url

        driver.quit()
        logger.info(f"第 {missionNumber} 個任務 - 網站訪問結束 - {datetime.now()}")
    except Exception as e:
        logger.error(f"第 {missionNumber} 個任務 - An error occurred: {e}")

def threaded_job(missionNumber):
    thread = threading.Thread(target=job, kwargs={'missionNumber': missionNumber})
    thread.start()

def schedule_job():
    start_time = datetime.now()
    end_time = start_time + timedelta(days=1)

    num_random_times = random.randint(150, 200)
    schedule_list = sorted([get_random_timestamp(start_time.timestamp(), end_time.timestamp()) for _ in range(num_random_times)])

    # 顯示排定的時間
    logger.info("開始新排程 - 規劃時間")
    logger.info(f"今日預計訪問次數: {num_random_times} 次")

    for i in range(len(schedule_list)):
        logger.info(f"排程時間清單：第 {i + 1} 個任務 - {schedule_list[i].strftime('%Y-%m-%d %H:%M:%S.%f')})")

    # 排程每個時間戳執行job
    for i in range(len(schedule_list)):
        schedule.every().day.at(schedule_list[i].strftime('%H:%M:%S')).do(lambda i=i: threaded_job(i + 1))