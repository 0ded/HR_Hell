import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

def connect(user, password):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(user, password)
        return server
    except:
        print("Error connecting to gmail")


def send_mail(subject, to_addr, text, user=("equaldegen@equaldegen.com", "degen_equality"), files=None):
    try:
        if user[0].split("@")[1].split(".")[0] != "gmail":
            raise Exception("Gmail address was not specified")
    except:
        raise Exception("Error getting Gmail address")

    msg = MIMEMultipart()
    msg['From'] = user[0]
    msg['To'] = to_addr
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = connect(user[0], user[1])
    try:
        server.sendmail(user[0], [to_addr], msg.as_string())
        server.close()
    except:
        print("Error sending mail")


def fake_send(subject, to_addr, text, user=("equaldegen@equaldegen.com", "degen_equality"), files=None):
    # for testing
    send_mail(subject, user[0], text, user, files)
