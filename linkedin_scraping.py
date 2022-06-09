import parameters
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep 
from selenium.webdriver.common.by import By
from parsel import Selector
from selenium.webdriver.common.keys import Keys

writer = csv.writer(open(parameters.result_file, 'w'))
writer.writerow(['name', 'title', 'location', 'ln_url'])

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(5)

driver.find_element(By.XPATH, '//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]')
sleep(3)

username_input = driver.find_element(By.NAME, 'session_key')
username_input.send_keys(parameters.username)
sleep(5)

password_input = driver.find_element(By.NAME, 'session_password')
password_input.send_keys(parameters.password)
sleep(5)

driver.find_element(By.XPATH, '//button[@class="sign-in-form__submit-button"]').click()
sleep(5)

#redirect to google.com to conduct search
driver.get('https://www.google.com/')
sleep(3)

#locating search bar
search_input = driver.find_element(By.NAME, "q")
search_input.send_keys(parameters.search_query)
sleep(5)

search_input.send_keys(Keys.RETURN)
sleep(5)

#extracint linkedin links
profiles = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')
profiles = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a[1]')
profiles = [profile.get_attribute('href') for profile in profiles]

for profile in profiles:
    driver.get(profile)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//title/text()').extract_first().split(' | ')[0].split(') ')[1]
    title = sel.xpath('//*[@class="text-body-medium break-words"]/text()').extract_first().strip()
    location = sel.xpath('//*[@class="pb2 pv-text-details__left-panel"]/span/text()').extract_first().strip()
    ln_url = driver.current_url

    print('\n')
    print(name)
    print(title) 
    print(location)
    print(ln_url)
    print('\n')

    writer.writerow([name, title, location, ln_url])


driver.quit()


