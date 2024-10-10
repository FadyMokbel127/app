from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from datetime import datetime

# Telegram Bot API token and chat ID
BOT_TOKEN = '7053936270:AAHGmMYo9DhPQKqiL7e0Y8RoXaAbu1hwq_Y'
CHAT_ID = '768606681'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

login_url = "https://register.must.edu.eg/StudentRegistrationSsb/ssb/registration"
username = "200013323"
password = "Df1272002."
code = input("Enter course code : ")
c4 = code[0:4]
c5 = code[4:10]
print(c4)
print(c5)

# Initialize the browser driver
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

# Load the login page
driver.get(login_url)

# Wait and click the "Student Self Service" link
wait = WebDriverWait(driver, 10)
register_link = wait.until(EC.presence_of_element_located((By.ID, 'classSearchLink')))
register_link.click()
term = wait.until(EC.presence_of_element_located((By.ID, 's2id_txt_term')))
term.click()
termc = wait.until(EC.presence_of_element_located((By.ID, 's2id_autogen1_search')))
time.sleep(1)
termc.send_keys(Keys.ENTER)
continuee = wait.until(EC.presence_of_element_located((By.ID, 'term-go')))
continuee.click()
time.sleep(5)
coursecode = wait.until(EC.visibility_of_element_located((By.ID, "s2id_autogen1")))
coursecode.send_keys(c4)
time.sleep(1)
coursecode.send_keys(Keys.ENTER)
coursenum = wait.until(EC.visibility_of_element_located((By.ID, "txt_courseNumber")))
coursenum.send_keys(c5)
coursenum.send_keys(Keys.ENTER)
with open(r"D:\Python\TeleLog\UniLog.txt", "a") as file:
    while True:
        time.sleep(2)
        
        # Re-locate the element to avoid stale element reference
        seat_info_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[@data-id='872166' and @data-property='status']")))
        seat_info = seat_info_td.get_attribute("title").strip(" LINKED")
        
        # Check if the seat information contains "0 of 50 seats remain"
        if "0 of " in seat_info_td.text:
            message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {seat_info}"
            print(message)
            file.write(f'{message}\n')
            file.flush()
        else:
            message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {seat_info}"
            print(message)
            send_telegram_message(message)
            send_telegram_message("https://register.must.edu.eg/StudentRegistrationSsb/ssb/registration")
            file.write(f'{message}\n')
            file.flush()
        
        # Refresh the search
        time.sleep(1)
        search_again = wait.until(EC.presence_of_element_located((By.ID, 'search-again-button')))
        search_again.click()
        time.sleep(2)
        search = wait.until(EC.presence_of_element_located((By.ID, 'search-go')))
        search.click()

# Close the driver after some time (if needed)
driver.quit()
