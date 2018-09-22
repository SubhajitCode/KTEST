import pdfkit
from selenium import webdriver
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

LOGIN_URL = "https://ktest.kreatryx.com/home"
chrome_path = r"G:\Projects\Python Projects\chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_path)

browser.get(LOGIN_URL)
cookies = pickle.load(open("cookies.pkl", "rb"))
google = "https://accounts.google.com/signin/oauth/identifier?client_id=129913025222-r1ldft5j7fk1pihuj8b5t2k7sroarda0.apps.googleusercontent.com&as=-6473c2c48b4f423e&destination=https%3A%2F%2Fktest.kreatryx.com&approval_state=!ChR0dmpGX1R2bGxlczhfN1ktdE9NdBIfTXg5dk5aMDZtOTRjVU9xWmlfQjdtUl9FZVVXaDdSVQ%E2%88%99AHw7d_cAAAAAWdK_J3a6jHdQ7RD2uYnpWJ-d602lZ7dr&passive=1209600&oauth=1&sarp=1&scc=1&xsrfsig=AHgIfE9bTm-r6pbeORh0ybPxUEMSABJWUQ&flowName=GeneralOAuthFlow"

browser.get(google)
for cookie in cookies:
    if "google" in cookie['domain']:
        browser.add_cookie(cookie)
browser.get(LOGIN_URL)
WebDriverWait(browser, 3000).until(EC.visibility_of_element_located(
    (By.XPATH, "//h4[contains(text(),'SIGN-UP / LOGIN')]")))
login_attempt = browser.find_element_by_xpath("//h4[contains(text(),'SIGN-UP / LOGIN')]")
login_attempt.click()
WebDriverWait(browser, 3000).until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(),'LOGIN WITH GOOGLE')]")))
login_attempt2 = browser.find_element_by_xpath("//button[contains(text(),'LOGIN WITH GOOGLE')]")
browser.execute_script("arguments[0].click();", login_attempt2)

WebDriverWait(browser, 3000).until(EC.visibility_of_element_located(
    (By.XPATH, "//button[contains(text(),'VIEW PROFILE')]")))
print("Manual logged in")
while browser != "null" :
    browser.get(LOGIN_URL)
    WebDriverWait(browser, 3000).until(EC.visibility_of_element_located(
        (By.XPATH, '//div[@class="test-legend"]')))
    print("Test legend located")
    test_legend = browser.find_element_by_xpath('//div[@class="test-legend"]')
    test_title_xpath = browser.find_element_by_xpath('//p[@class="navbar-brand"]').get_attribute("outerHTML")
    test_title = "full/"+browser.find_element_by_xpath('//p[@class="navbar-brand"]').text
    test_title = test_title.replace("Solution","")
    print(test_title)
    test_title=test_title + ".pdf"

    options = {
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],

    }
    unattempted_Questions = browser.find_elements_by_xpath('//span[@class="indicator unattempted" or @class="indicator unvisited" or @class="indicator attempted"]')
    question_string = "<head>"
    heads = browser.find_elements_by_xpath('//style')
    for index2 in range(len(heads)):
        question_string = question_string + heads[index2].get_attribute("outerHTML")
    question_string = question_string + "</head>"
    question_string = question_string + "<body>"+test_title_xpath.replace(" - Solution","")
    solution_string = question_string
    for index in range(1,len(unattempted_Questions)):
        unattempted_Question = unattempted_Questions[index]
        browser.execute_script("arguments[0].click();", unattempted_Question)
        # unattempted_Question.click()
        WebDriverWait(browser, 3000).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@class="que-container card"]')))
        time.sleep(1);
        question = browser.find_element_by_xpath('//div[@class="que-container card"]').get_attribute("outerHTML")
        question_number = browser.find_element_by_xpath('//h4[@class="pull-left inline" and contains(text()," Question No. ")]').get_attribute("outerHTML")
        solution = question_number+browser.find_element_by_xpath('//div[@class="sol-container card"]').get_attribute("outerHTML")
        question_string = question_string + question
        solution_string = solution_string + solution

    question_string = question_string+"</body>"
    solution_string = solution_string+"</body>"
    pdfkit.from_string(question_string, test_title, options=options)
    pdfkit.from_string(solution_string, test_title.replace(".pdf"," Solution.pdf") , options=options)
























