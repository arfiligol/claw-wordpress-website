import time
from datetime import datetime, timedelta
import schedule
import atexit
from dotenv import load_dotenv
load_dotenv()
import os

from job import schedule_job, logger

def exit_handler():
    logger.info("應用程式結束")

atexit.register(exit_handler)

logger.info(f"應用程式開始運行，預計開始規劃的時間點：{os.getenv('CRAWLER_START_TIME', '00:00:00')}")

while True:
    # 每天凌晨0點執行schedule_job
    schedule.every().day.at(os.getenv("CRAWLER_START_TIME", "00:00:00")).do(schedule_job)
    current_date = datetime.now().date()
    parsed_time = datetime.strptime(os.getenv('CRAWLER_START_TIME', '00:00:00'), "%H:%M:%S").time()
    end_time = datetime.combine(current_date, parsed_time) + timedelta(hours=23, minutes=45)
    
    while True:
        if datetime.now() >= end_time:
            break
        schedule.run_pending()
        time.sleep(1)

    # 清除所有排程
    logger.info(f"清除今日所有排程，準備下一次排程...")
    schedule.clear()