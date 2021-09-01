import os
import time
import smtplib
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    detector = Instock()
    detector.instock_detector()