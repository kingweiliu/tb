# coding=utf8
__author__ = 'ljw'

import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import random
import smtplib
import logging

logging.basicConfig(format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    level=logging.DEBUG, filename="email.log")

# 加载以用户名\t密码格式的电邮账户列表
def load_maillist():
    ret = []
    f = open("emaillist.cfg")
    for l in f:
        if l[0] == "#":
            continue
        parts = l.strip().split()
        ret.append(parts)
    f.close()
    return ret

# 加载目的电子邮件列表
def load_tolist(maillist):
    f =open(maillist)
    yield "514861870@qq.com"
    yield "txwd0033@163.com"
    for l in f:
        yield l.strip()
    f.close()

def encapsule_mail(to_addr, from_addr):

    msg = MIMEMultipart()
    msg["Subject"] = Header("每天一个苹果，有益身体健康", "utf-8")
    msg["From"] = from_addr
    html = """
    <html>
    <body>
    目前空气质量很差，要注意身体健康，多补充维生素；优质的苹果等您选购
    <a href='http://shop142605038.taobao.com'>http://shop142605038.taobao.com</a>
    </body>
    </html>
    """

    msg_html = MIMEText(html, "html", "utf-8")
    msg.attach(msg_html)
    return  msg.as_string()



def start_send(maillist):
    fromlist = load_maillist()
    print fromlist
    for to in load_tolist(maillist):
        host, user, passwd, fromemail = random.sample(fromlist, 1)[0]
        print to
        msg = encapsule_mail(to, fromemail)
        try:
            smtp = smtplib.SMTP(host, timeout=3000)
            smtp.login(user, passwd)
            smtp.sendmail(fromemail, to, msg)
            logging.info("[from:%s][to:%s]ok", fromemail, to)
        except Exception as ex:
            logging.warning("[from:%s][to:%s]failed, msg:%s", fromemail, to, ex)


if __name__ == "__main__":
    start_send("h800_999.txt")
#
#
#
# msg = MIMEMultipart()
# msg["Subject"] = Header("每天一个苹果，有益身体健康,今天你吃苹果了吗？", "utf-8")
#
#
# html = """
# <html>
# <body>
# 目前空气质量很差，要注意身体健康，多补充维生素；欢迎你选购
# <a href='http://shop142605038.taobao.com'>http://shop142605038.taobao.com</a>
# <img src="http://www.syly8.com/a.png?qq=514861870@qq.cm&time=2015"/>
# 我都不知道他怎么判断
# </body>
# </html>
# """
#
# msg_html = MIMEText(html, "html")
#
# msg.attach(msg_html)
# print msg.as_string()
#
# smtp = smtplib.SMTP("smtp.163.com")
# smtp.login("txwd0033", "Ljwisno12016")
# smtp.sendmail("txwd0033@163.com", "514861870@qq.com", msg.as_string())
