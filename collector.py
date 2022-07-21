import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys

import mailing
from utils import get_json, write_json
import re

details = get_json("./details.json")
settings = get_json("./settings.json")
message = get_json("./message.json")
white_words = get_json("./words_that_indicate_someone_is_looking_for_work.json")["words"]


def do_send(flags: dict):
    print("sending mails:\n")
    while len(details["mails_fetched"]) != 0 and not flags["fake_send"]:
        print(len(details["mails_fetched"]), "left")
        i = details["mails_fetched"][0]
        if i not in [j.lower() for j in details["mails_sent"]]:
            if flags["immediate_send"]:
                mailing.send_mail(message["subject"], i, message["message"],
                                  (details["gmail"], details["gmail_password"]), details["attached_pdf"])
                details["mails_sent"].append(i)
                details["mails_fetched"].remove(i)
            else:
                mailing.safe_send_mail(message["subject"], i, message["message"], (details["gmail"], details["gmail_password"]), details["attached_pdf"])
                details["mails_sent"].append(i)
                details["mails_fetched"].remove(i)
        else:
            details["mails_fetched"].remove(i)
    if flags["fake_send"]:
        for i in details["mails_fetched"]:
            mailing.fake_send(message["subject"], i, message["message"],
                              (details["gmail"], details["gmail_password"]), details["attached_pdf"])
    write_json("./details.json", details)


def collect(passes: int = 1, flags: dict = {}):
    if check_mail(flags["add"]):
        details["mails_fetched"].extend([flags["add"]])
        write_json("./details.json", details)
        return
    browser = base_connect(details["search_url"])

    signin_steps(browser, settings["un_xpath"], settings["pw_xpath"], details["li_username"], details["li_password"],
                 settings["si_btn_path"])
    mails = []

    sleep(0.5)

    for j in range(passes):
        webdriver.ActionChains(browser).key_down(Keys.PAGE_DOWN).perform()
        sleep(0.3)

    posts = get_all_posts(browser)
    temp = get_comments(posts)
    browser.close()
    for mail in temp:
        if mail[0] not in [i[0] for i in mails]:
            mails.append(mail)
    # mails = list(dict.fromkeys(mails))
    print("fetched: ", [i[0] for i in mails])
    details["mails_fetched"].extend([i[0] for i in mails])
    write_json("./details.json", details)


def get_comments(posts):
    comments = []
    for i, post in enumerate(posts):
        print("collecting mails:",  "{}/{}".format(i, len(posts)))
        try:
            # print(post[1].text)
            btns = post[1].find_elements(
                By.TAG_NAME,
                "button")
            for btn in btns:
                if "comments" in [i.lower() for i in btn.text.split()]:
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
        print("found:", len(comments))
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


def check_mail(string: str):
    if (re.fullmatch('\S+@\S+', string)) and \
            string not in get_json("./details.json")["mails_sent"]:
        if ":" in string:
            string = string.split(":")[1]
        return string
    return None
