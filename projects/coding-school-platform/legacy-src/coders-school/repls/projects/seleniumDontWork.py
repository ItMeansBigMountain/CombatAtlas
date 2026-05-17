from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#CHROME WEBDRIVER OPTIONS
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)



#go to this website
driver.get("https://virtualglobetrotting.com/")

#let the code chill for 10 seconds
time.sleep(10)


searchbar = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/form/div/span/input[2]')

searchbar.click()

searchvar = input("Please enter a name of someone you want to look up : ")

searchbar.send_keys(str(searchvar))

submitsearch = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/form/div/a[1]')

time.sleep(3)

print('searched for '+ searchvar)