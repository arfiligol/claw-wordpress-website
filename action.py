import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_scroll(driver):
    max_distance = 500
    min_distance = 100
    random_distance = random.randint(min_distance, max_distance)
    steps = 10
    distance_per_step = random_distance / steps
    delay_per_step = 0.01  # seconds

    for _ in range(steps):
        driver.execute_script(f"window.scrollBy(0, {distance_per_step});")
        time.sleep(delay_per_step)

def random_click(driver):
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://cdrap.cxcxc.info"]')
    clicked_links = set()

    while len(links) > len(clicked_links):
        available_links = [link for idx, link in enumerate(links) if idx not in clicked_links]
        random_link = random.choice(available_links)

        clicked_links.add(links.index(random_link))

        try:
            random_link.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            break
        except:
            if len(links) == len(clicked_links):
                break

def random_wait(min_seconds, max_seconds):
    random_time = random.uniform(min_seconds, max_seconds)
    time.sleep(random_time)