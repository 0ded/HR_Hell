# HR HELL

A selenium based python script, 
designed to located HR mails on linkedin.com, and mass send them
job applications.

## How to
- clone this repo

- [Download](https://github.com/mozilla/geckodriver/releases) the geckodriver based on your os

- Place it in the cloned folder and change it's name to "geckodriver"
  (no suffix)

- In detail.json change the following:
```json
  "li_username": Your linkedin username or mail here,
  "li_password": Your linkedin password here,
  "gmail": Your gmail mail here,
  "gmail_password": Your gmail password here,
  "search_url": Search url here,
  "attached_pdf": An array of all the files you wish to add to the mail
```
- Now you are ready to run

```bash
python main.py
```

## IMPORTANT!!

- Must have python 3.6 or any newer version
- Must have selenium and re
- You must use gmail, don't use your current employer mail address
- Make sure the "Less secure apps" option in your google account is on
  (more info can be found [here](https://www.dev2qa.com/how-do-i-enable-less-secure-apps-on-gmail/))
- The url **must be a linkedin sign-in page.** i.e, must look like this:
[signin page](/img.png)


