#coding:utf8
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

mail_info = {
    "from": "939750339@qq.com",
    "hostname": "smtp.qq.com",
    "username": "939750339@qq.com",
    "password": "esclmnuhbhxhbebg",
    "mail_encoding": "utf-8"
}

def send_mail(to_list="uunique7@qq.com",mail_subject="Subject",mail_text="hello, this is a test email, sended by py"):
  
  msg = MIMEText(mail_text, "plain", mail_info["mail_encoding"])
  msg["Subject"] = Header(mail_subject, mail_info["mail_encoding"])
  msg["from"] = mail_info["from"]
  msg["to"] = ";".join(to_list)

  try:
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)

    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    smtp.sendmail(mail_info["from"], to_list, msg.as_string())

    return True

  except Exception, e:
    print str(e)
    return False
  finally:
    smtp.quit()

if __name__ == '__main__':
    send_mail()