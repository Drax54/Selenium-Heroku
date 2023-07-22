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
            # driver = webdriver.Chrome()

            driver = webdriver.Chrome(service=service, options=chrome_options)
           
            driver.get(url)
            print("Waiting for the Source code of:", url)
            flash("Waiting for the Source code of: {}".format(url))
            time.sleep(5)
            html = driver.page_source
            time.sleep(2)
            soup = bs4.BeautifulSoup(html, "html.parser")
            time.sleep(2)
            video_data = ''
            # # Click on the "Allow cookies" button

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "myDynamicElement"))
                )
                
                video_data = soup.find_all('video')[0]

            except TimeoutException:
                print("Element not found after wait")  

            # try:
            #     video_data = soup.find_all('video')[0]
            
            # except Exception as e:
            #     video_data = soup.find_all('video') 

            video_src = video_data['src']
            
            print("Downloading video:", video_src)
            flash("Downloading video: {}".format(video_src))
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