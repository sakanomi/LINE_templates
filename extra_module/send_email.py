import urllib.request
import smtplib
from email.utils import formatdate
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import re

import configparser

#設定ファイルの読み込み
cfg = configparser.ConfigParser()
cfg.read('config.ini')

csv_tmp = 1#1にするとユーザー情報の添付をする。

def EMAIL(user_id=None, user=None, data=None, nowdate=None, img_url_ls=None):
    #お客様情報
    user_data = data

    #送り元
    from_email=cfg["EMAIL"]["FROM"]
    from_password=cfg["EMAIL"]["PASS"]

    #送り先：宛先二人まで
    to_email=[cfg["EMAIL"]["TO1"], cfg["EMAIL"]["TO2"]]

    nownow = nowdate + ":00"
    # print(data)
    data2 = re.sub("\\D", "", nownow)
    nowdate = data2[:4] + "年" + data2[4:6] + "月" + data2[6:8] + "日 " + data2[8:10] + "時" + data2[10:12] + "分頃"

    #メールの内容
    subject=""#件名
    message=""#メッセ―ジの内容【HTML形式】
    msg = MIMEMultipart()
    body = MIMEText(message, "html")
    msg.attach(body)
    msg["Subject"] = subject
    msg["To"] = ",".join(to_email)
    msg["From"] = from_email

    name_ls = ["image1", "image2", "image3", "image4", "image5"]


    for i in range(len(img_url_ls)):
        # 添付ファイルの設定
        url = img_url_ls[i]
        name = name_ls[i]+".png"
        attachment = MIMEBase('image', 'png')
        file = urllib.request.urlopen(url).read()
        attachment.set_payload(file)
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=name)
        msg.attach(attachment)

    """
    if csv_tmp == 1:
        csv_url = put_to_csv(user_id)
        name = user_id + ".csv"
        mine = {'type': 'text', 'subtype': 'comma-separated-values'}
        attachment = MIMEBase(mine['type'], mine['subtype'])
        file = urllib.request.urlopen(csv_url).read()
        attachment.set_payload(file)
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=name)
        msg.attach(attachment)
    """

    # gmailへ接続(SMTPサーバーとして使用)
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.starttls()  # SMTP通信のコマンドを暗号化し、サーバーアクセスの認証を通す
    gmail.login(from_email, from_password)
    gmail.send_message(msg)