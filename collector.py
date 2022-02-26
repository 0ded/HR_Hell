import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import re

def collect():
    browser = base_connect(
        "https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2Fhashtag%2F%3Fkeywords%3D%25D7%259B%25D7%2595%25D7%259C%25D7%2590%25D7%259C%25D7%2599%25D7%2599%25D7%25A7&fromSignIn=true&trk=cold_join_sign_in"
        "=true&trk=cold_join_sign_in")

    details = get_details("./details.json")
    signin_steps(browser, '//*[@id="username"]', '//*[@id="password"]', details["username"], details["password"],
                 '/html/body/div/main/div[2]/div[1]/form/div[3]/button')
    posts = get_all_posts(browser)
    get_comments(posts)


def get_comments(posts):
    comments = []
    for post in posts:
        print("-------------------")
        print(post[0])
        print("======================")
        try:
            # print(post[1].text)
            btns = post[1].find_elements(
                By.TAG_NAME,
                "button")
            for btn in btns:
                if "comments" in btn.text:
                    btn.click()

        except selenium.common.exceptions.NoSuchElementException:
            print("=--=-=-=-=-=-=- Fail")
        except selenium.common.exceptions.StaleElementReferenceException:
            pass

        sleep(1)
        for s in post[1].text.split():
            # print(s)
            if check_mail(s) is not None:
                comments.append(s)
        # print(post[1].text)
        print(comments)
    return

def get_all_posts(browser: webdriver):
    sleep(1.5)
    posts = browser.find_elements(By.CLASS_NAME, "relative")
    out = []
    for post in posts:
        txt = ""
        c_txt = []
        try:
            txt = post.find_element(By.CLASS_NAME, "break-words").text
        except selenium.common.exceptions.NoSuchElementException:
            pass
        else:
            out.append((txt, post))
    return out


def base_connect(site):
    browser = webdriver.Firefox(executable_path='./geckodriver')
    browser.maximize_window()
    # browser.set_window_position(0, 0)
    sleep(0.2)
    browser.get(site)
    return browser


def signin_steps(browser: webdriver, username_xpath, password_xpath, username, password, button_xpath=None):
    uf = browser.find_element(By.XPATH, username_xpath)
    sleep(0.2)
    uf.send_keys(username)
    pw = browser.find_element(By.XPATH, password_xpath)
    sleep(0.2)
    pw.send_keys(password)
    pw.find_element(By.XPATH, button_xpath).click()


def get_details(json_path) -> dict:
    f = open(json_path, "r")
    s = json.load(f)
    f.close()
    return s


def check_mail(string):
    if (re.fullmatch('\S+@\S+', string)):
        return string
    return None
