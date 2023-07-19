import os
import re
import requests, bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import chromedriver_autoinstaller


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, send_file


# set chrome options

# driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get("https://medium.com")
# print(driver.page_source)
# print("Finished!")

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        url = request.form.get('url')

        # Set up Selenium driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

# chromedriver_autoinstaller.install()

        service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for the "Allow cookies" button to be clickable
        allow_cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Allow all cookies")]')))

        # Click on the "Allow cookies" button
        allow_cookies_button.click()

        html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(html, "html.parser")
        video_data = soup.find_all('video')[0]
        video_src = video_data['src']

        # Download the video
        response = requests.get(video_src)

        file_name = "downloads.mp4"

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print("Video downloaded successfully.")
        else:
            print("Failed to download the video.")

        download_link = request.host_url + 'download'

        return render_template('result.html', download_link=download_link)

    return render_template('index.html')

@app.route('/download')
def download():
    file_path = 'downloads.mp4'
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
   app.run(debug=True, port=port)