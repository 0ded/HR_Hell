import smtplib

def connect(user, password):
    #connects you to gmail
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(user, password)
        return server
    except:
        print("Error connecting to gmail")

def send_mail(subject, to_addr, text, user=("equaldegen@equaldegen.com", "degen_equality")):
    #sends a mail to "to_addr" from "user" with "text" and "subject"
    #"user" is a tupple user[0] is a gmail address user[1] is the password

    try:
        if(user[0].split("@")[1].split(".")[0] != "gmail"):
            raise Exception("Gmail address was not specified")
    except:
        raise Exception("Error getting Gmail address")

    body = "\r\n".join((
        "from: %s" % user[0],
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        text
    ))

    server = connect(user[0], user[1])
    try:
        server.sendmail(user[0], [to_addr], body)
        server.close()
    except:
        print("Error sending mail")
