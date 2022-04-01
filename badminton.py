from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from datetime import datetime, timedelta



settings = json.load(open('settings.json'))
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


correct_dates = []
for val in settings['desired_times']:
    for days in settings['desired_days']:
        print(val, days)
        correct_dates.append(datetime.strptime(days + " " + str(val), '%d/%m/%Y %H'))

correct_dates = sorted(correct_dates)


def book_court(val):
    time.sleep(3)
    val.find_element(By.CLASS_NAME, 'btn-primary').click()
    print('clicked')
    time.sleep(3)
    driver.refresh()
    time.sleep(4)
    driver.find_element(By.XPATH, '//*[@id="btnAccept"]').click()
    print("waiver")
    time.sleep(2)
    driver.refresh()
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div[2]/form[2]/div[2]/button[2]').click()
    time.sleep(1)
    driver.refresh()
    print("start of checkout")
    driver.find_element(By.XPATH, '//*[@id="checkoutButton"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[5]/div/div/div[2]/button[2]').click()


def login():
    driver.find_element(By.XPATH, '//*[@id="loginLink"]').click()
    driver.find_element(By.XPATH, '//*[@id="section-sign-in-first"]/div[6]/div/button').click()
    driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(settings['usernames'])
    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(settings['passwords'])
    driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div[2]/form/button').click()
    time.sleep(2)

booked = False

for datetimer in correct_dates:
    while not booked:
        try:
            driver.get(settings['url'])
            driver.find_element(By.XPATH, '//*[@id="loginLink"]')
            login()
        except NoSuchElementException:
            pass
        search_scope = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div[1]/div[2]/section/div')
        indicies = []
        index = 0
        for val in search_scope.find_elements(By.CLASS_NAME, 'card'):
            try:
                val.find_element(By.CLASS_NAME, 'btn-primary')
                day_month = val.find_element(By.CLASS_NAME, 'card-title').text
                real_time = val.find_element(By.CLASS_NAME, 'text-muted').text
                real_time = real_time.split('-')[0][0:-1]
                date = datetime.strptime(day_month + " " + real_time, "%A, %B %d, %Y %I:%M %p")
                date = date.replace(minute=0)
                print(date.strftime("%d/%m/%Y %H"), correct_dates[0].strftime("%d/%m/%Y %H"))
                if date == datetimer:
                    indicies.append(index)
            except NoSuchElementException:
                print('No button found')
            index += 1
        for val in indicies:
            driver.get(settings['url'])
            search_scope = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[3]/div[1]/div[2]/section/div')
            book_court(search_scope.find_elements(By.CLASS_NAME, 'card')[val])
            booked = True
        time.sleep(30)