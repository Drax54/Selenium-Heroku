import os
import re
import requests, bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request, send_file
import webbrowser
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, render_template, send_file, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'rhul'

@app.route('/', methods=['GET', 'POST'])

def index():
    try:
        if request.method == 'POST':
            url = request.form.get('url')

            # Set up Selenium driver
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")

            # webbrowser.open(url)

            # chromedriver_autoinstaller.install()

            service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            driver = webdriver.Chrome()

            # driver = webdriver.Chrome(service=service, options=chrome_options)
           
            driver.get(url)
            video_data = ''
            video_src = ''
            # # Click on the "Allow cookies" button
            try:
                timeout = 10
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
                time.sleep(2)
                html = driver.page_source
                soup = bs4.BeautifulSoup(html, "html.parser")
                time.sleep(2)

                video_data_list = soup.find_all('video')

                if len(video_data_list) > 0:  # Only proceed if the list is not empty
                    video_data = video_data_list[0]
                    print(video_data)
                    video_src = video_data['src']
                else:
                    print("No video tags found on the page.")

            except TimeoutException:
                print("Element not found after wait")  
 
            response = requests.get(video_src)
            
            if response.status_code == 200:
                print("Saving video...")
                with open('downloads.mp4', 'wb') as f:
                    f.write(response.content)
                
                print("Video downloaded!")
            
            else:
                print("Failed to download video")
            
            download_link = request.host_url + 'download'
            return render_template('result.html', download_link=download_link)
        
    except TimeoutException:
        print("Timeout waiting for allow cookies button")
        flash("Timeout waiting for allow cookies button")
          
    except Exception as e:
        print("Unknown exception:", e)
        flash("Unknown exception: {}".format(e))
     
    return render_template('index.html')

@app.route('/download')
def download():
    file_path = 'downloads.mp4'
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)