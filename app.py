from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from flask import Flask, request, jsonify
import json
import os
import time

app = Flask(__name__)

branch = ""

url = 'https://www.wordsapi.com/#try'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
if branch == "dev":
    driver = webdriver.Chrome(options=chrome_options)
else:
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=chrome_options)

print("driver get")
driver.get(url)

def init():
    global url
    print("in init")
    global driver, chrome_options
    if branch == "dev":
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=chrome_options)

    driver.get(url)

print("loaded")
@app.route('/')
def home():
    print(" in home")
    return "connected"


@app.route('/app', methods=['POST'])
def index():

    print("in app")
    global driver
    req = request.get_json()
    word = ""
    word = req['word']

    print(word)

    try:
        print(driver.title)
        driver.refresh()
    except WebDriverException:
        init()
    
    print("url opened")
    try:
        print("get url")
        print(url)
        
        xpath_input = "//*[@id=\"word\"]"
        xpath_syn = "/html/body/div[1]/div[3]/div/form/div/div[1]/div[2]/select/option[3]"
        xpath_button = "//*[@id=\"getWord\"]"
        print("send keys")
        input_fd = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, xpath_input)))
        input_fd.clear()
        input_fd.send_keys(word)
        print("Sleep")
        time.sleep(2)
        print("click synonyms")
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,xpath_syn)))
        driver.find_element_by_xpath(xpath_syn).click()
        print("click ")
        WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,xpath_button)))
        driver.find_element_by_xpath(xpath_button).click()
        for i in range(1):
            print(i)
            time.sleep(1)

        WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'exampleLink')))
        synonyms = driver.find_elements_by_class_name('exampleLink')
        output = ""
        x = 0
        count = 0
        for item in synonyms:
            if(x < 12):
                print("ignore:",item.text)
                x += 1
            else:
                output += item.text
                output.replace("\"","")
                output += ", "
                count += 1
            #output.strip("\"")

        print(output)
        if(len(output) == 0):
            output = "No Results"

        return jsonify(
            output = output,
            count = count
        )
        

    except Exception as e:
        driver.close()
        print(e.__doc__)
        return "Something went wrong, Please try again!!"


if __name__ == '__main__':
    #app.debug = True
    app.run()