from selenium import webdriver
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")



from selenium.webdriver.chrome.service import Service

service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# set chrome options

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://medium.com")
print(driver.page_source)
print("Finished!")