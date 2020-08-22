from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, request
import json
import os

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
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.thesaurus.com/browse/{}?s=t".format(word)
    output = ""
    print("url opened")
    try:
        driver.get(url)
        xpath_for_synonyms = '//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/ul'
        xpath_for_suggestions = '//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/div/h2[2]'
        items = driver.find_element_by_xpath(xpath_for_synonyms)
        chk = driver.find_elements_by_xpath(xpath_for_suggestions)

        if(len(chk) > 0):
            print("Suggested Alternatives")
            output += "Suggested Alternatives\n"
        
        else:
            print("Synonyms")
            output += "Synonyms\n"

        sym = items.text
        lis = sym.split("\n")
        for i in range(len(lis)):
            print(lis[i])
            output += lis[i]
            output += "\n"
        
        
        return output

    except NoSuchElementException:
        return "D.N.E"


if __name__ == '__main__':
    app.debug = True
    app.run()