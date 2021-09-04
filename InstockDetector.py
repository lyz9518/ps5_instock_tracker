import os
import time
import smtplib
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class InstockDetector:
    def __init__(self):
        self.last_timestamp = None
        # We are using nowinstock for checking availability
        self.url = 'https://www.nowinstock.net/videogaming/consoles/sonyps5/'
        
    def send_warning(self, seller):
        '''
            Send instock warning email to end-user
        '''
        HOST_EMAIL = os.environ.get('PS5TRACKER')
        HOST_EMAIL_PWD = os.environ.get('PS5TRACKERPWD')
        
        msg = EmailMessage()
        msg['Subject'] = f'Play Station 5 Instock at {seller}'
        msg['From'] = HOST_EMAIL
        msg['To'] = [HOST_EMAIL, "xinfengl@umich.edu", "vincentdwy@gmail.com"]
        msg.set_content(f'{seller} has PS5 in stock. RUSH!!!!!')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(HOST_EMAIL, HOST_EMAIL_PWD)

            smtp.send_message(msg)
        return
            
    def start_monitoring(self):
        '''
            Download Chromedriver and paste its path to chromedriver var.
        '''
        while True:
            chromedriver = '/Users/lyz9518/Documents/chromedriver'
            driver = webdriver.Chrome(chromedriver)
            driver.get(self.url)
            time.sleep(1) # wait for cookies confirmation
            elements = driver.find_elements_by_class_name('cc_b_ok')
            elements[0].send_keys(Keys.ENTER)

            # Trace the most recent instock history

            data = driver.find_element(By.XPATH, '//div[@id="DisplayHistory"]/div[@id="data"]/table/tbody')
            last_record = data.find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')

            timestamp = last_record[0].text #e.g. ['Aug', '31', '-', '10:08', 'AM', 'EST']
            seller = last_record[1].text.split()[0]

            # New Instock Detected, Send Warning Email
            if self.last_timestamp != None:
                if self.last_timestamp != timestamp: # new instock info appears!
                    self.last_timestamp = timestamp
                    self.send_warning(seller)
                    print("Warning Email Sent!")
                    time.sleep(1200) # keep the web for displaying purpose for 10mins
                    driver.close()
                    break
                
            self.last_timestamp = timestamp
            driver.close()
            
            # Extend the check cycle to 1.5mins
            time.sleep(5)
        return
        