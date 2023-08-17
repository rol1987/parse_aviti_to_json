from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import main

def connect(url, full_path_chromedriver, frequency, sity, room, min_floor, max_floor):
    caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "normal"
    # caps["pageLoadStrategy"] = "eager" 
    caps["pageLoadStrategy"] = "none"

    useragent = UserAgent()
    option = webdriver.ChromeOptions()

    # option.add_argument(f"user-agent={useragent.random}")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36")
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = Service(full_path_chromedriver)
    driver = webdriver.Chrome(service = s, options = option)

    # Подключаем Selenium
    try:
        driver.get(url)
        time.sleep(5)
    except:
        print('Ошибка соединения с сервером/ Попытка повторного подключения....')
        main.restart(frequency, sity, room, min_floor, max_floor)
    finally:
        driver.close
        driver.quit
    return driver