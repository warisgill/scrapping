from selenium import webdriver
from bs4 import BeautifulSoup
import time
service_args = [
    '--proxy=62.113.208.183:3128',
    '--proxy-type=http',
    ]

driver = webdriver.PhantomJS(service_args=service_args)
time.sleep(20)
driver.get("https://www.whatismyip.com")
soup = BeautifulSoup("html.parser",driver.page_source)
print(soup.prettify())
driver.quit()

print("ended")
