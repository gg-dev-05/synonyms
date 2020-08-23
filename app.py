from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from flask import Flask, request
import json
import os
import time

app = Flask(__name__)



@app.route('/')
def home():

    return "connected"


@app.route('/app', methods=['POST'])
def index():

    req = request.get_json()
    word = ""
    word = req['word']

    print(word)
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)
    # url = "https://www.thesaurus.com/browse/{}?s=t".format(word)
    url = 'https://www.wordsapi.com/#try'
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    

    print("url opened")
    try:
        print("get url")
        print(url)
        driver.get(url)
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
        for i in range(3):
            print(i)
            time.sleep(1)

        WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'exampleLink')))
        synonyms = driver.find_elements_by_class_name('exampleLink')
        output = ""
        x = 0
        for item in synonyms:
            if(x < 12):
                print("ignore:",item.text)
                x += 1
            else:
                output += item.text
                output.replace("\"","")
                output += "\n"
            #output.strip("\"")

        print(output)
        if(len(output) == 0):
            output = "No Results"

        driver.close()
        return output
        # # xpath_for_synonyms = '//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/ul'
        # # xpath_for_suggestions = '//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/div/h2[2]'
        # print("find elements by synonyms")
        # items = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath_for_synonyms)))
        # print("find elements by suggestions")
        # chk = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath_for_suggestions)))

        # print("check value of chk")
        # if(len(chk) > 0):
        #     print("Suggested Alternatives")
        #     output += "Suggested Alternatives\n"
        
        # else:
        #     print("Synonyms")
        #     output += "Synonyms\n"

        # print("add all")
        # sym = items.text
        # lis = sym.split("\n")
        # for i in range(len(lis)):
        #     print(lis[i])
        #     output += lis[i]
        #     output += "\n"
        
        
        # driver.close()
        # return output

    except Exception as e:
        driver.close()
        print(e.__doc__)
        return "Something went wrong, Please try again!!"


if __name__ == '__main__':
    app.debug = True
    app.run()