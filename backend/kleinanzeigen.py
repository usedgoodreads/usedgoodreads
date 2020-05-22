import time
import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)

driver.get("https://www.ebay-kleinanzeigen.de/s-buecher-zeitschriften/c76")  # books

gdpr = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "gdpr-banner-accept")))
gdpr.click()

search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "site-search-query")))
search.send_keys("Harry Potter")
search.send_keys(Keys.RETURN)

time.sleep(5)

results = driver.find_elements_by_id("srchrslt-adtable")
assert len(results) == 1
result = results[0]
assert result.tag_name == "ul"

for item in result.find_elements_by_class_name("lazyload-item"):
    main = item.find_element_by_class_name("aditem-main")
    a = main.find_element_by_tag_name("a")
    print(a.text)
    print(a.get_attribute("href"))
    desc = main.find_element_by_tag_name("p").text
    print(desc)

    details = item.find_element_by_class_name("aditem-details")
    price = details.find_element_by_tag_name("strong").text
    print(price)

    date = item.find_element_by_class_name("aditem-addon").text
    print(date)

    print()


driver.close()
