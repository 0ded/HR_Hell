import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
import json
import re


def collect(passes: int = 1):
    details = get_details("./details.json")

    browser = base_connect(details["search_url"])

    signin_steps(browser, '//*[@id="username"]', '//*[@id="password"]', details["username"], details["password"],
                 '/html/body/div/main/div[2]/div[1]/form/div[3]/button')
    mails = []
    sleep(0.5)
    for j in range(passes):
        webdriver.ActionChains(browser).key_down(Keys.PAGE_DOWN).perform()
        sleep(0.1)
    posts = get_all_posts(browser)
    temp = get_comments(posts)
    for mail in temp:
        if mail[0] not in [i[0] for i in mails]:
            mails.append(mail)

    # mails = list(dict.fromkeys(mails))
    print([i[0] for i in mails])
    browser.close()


def get_comments(posts):
    comments = []
    for post in posts:
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
        except selenium.common.exceptions.StaleElementReferenceException or \
               selenium.common.exceptions.ElementClickInterceptedException:
            pass

        sleep(0.2)
        for s in post[1].text.split():
            # print(s)
            if check_mail(s) is not None:
                comments.append((s, post[1].text))
        # print(post[1].text)
    return comments


def get_all_posts(browser: webdriver):
    sleep(0.5)
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
