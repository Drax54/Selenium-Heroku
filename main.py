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

            # If we're running in a server environment...
            if os.environ.get("IS_PRODUCTION") == "true":
                print("this is server")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")

                chromedriver_autoinstaller.install()

                service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                print("this is local")
                driver = webdriver.Chrome()

            driver.get(url)
            print("Waiting for the Source code of:", url)
            flash("Waiting for the Source code of: {}".format(url))
            time.sleep(5)

            html = driver.page_source
            time.sleep(5)
            soup = bs4.BeautifulSoup(html, "html.parser")

            video_data = soup.find_all('video')
            time.sleep(5)

            if video_data:  # if the list is not empty
                video_src = video_data[0]['src']

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
            else:
                flash("No video found.")
    except Exception as e:
        flash("An error occurred: {}".format(e))
    return render_template('index.html')

# def index():
#     try:
#         if request.method == 'POST':
#             url = request.form.get('url')

#             # Set up Selenium driver
#             chrome_options = webdriver.ChromeOptions()
#             chrome_options.add_argument("--headless")
#             chrome_options.add_argument("--disable-dev-shm-usage")
#             chrome_options.add_argument("--no-sandbox")

#             chromedriver_autoinstaller.install()

#             service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
#             chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

#             # Include service and chrome_options as parameters
           
#             try:
#                 driver = webdriver.Chrome()
#             except:
#                 driver = webdriver.Chrome(service=service, options=chrome_options)
            
#             driver.get(url)
#             print("Waiting for the Source code of:", url)
#             flash("Waiting for the Source code of: {}".format(url))
#             time.sleep(5)
            
#             html = driver.page_source
#             time.sleep(5)
#             soup = bs4.BeautifulSoup(html, "html.parser")

#             video_data = soup.find_all('video')
#             time.sleep(5)

#             if video_data:  # if the list is not empty
#                 video_src = video_data[0]['src']

#                 print("Downloading video:", video_src)
#                 flash("Downloading video: {}".format(video_src))
#                 response = requests.get(video_src)

#                 if response.status_code == 200:
#                     print("Saving video...")
#                     with open('downloads.mp4', 'wb') as f:
#                         f.write(response.content)

#                     print("Video downloaded!")

#                 else:
#                     print("Failed to download video")

#                 download_link = request.host_url + 'download'
#                 return render_template('result.html', download_link=download_link)
#             else:
#                 flash("No video found.")
#     except Exception as e:
#         flash("An error occurred: {}".format(e))
#     return render_template('index.html')


@app.route('/download')
def download():
    file_path = 'downloads.mp4'
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)





# set chrome options

# driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get("https://medium.com")
# print(driver.page_source)
# print("Finished!")