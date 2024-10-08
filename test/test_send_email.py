"""
Description: 
    
-*- Encoding: UTF-8 -*-
@File     ：test_send_email.py
@Author   ：King Songtao
@Time     ：2024/10/8 下午3:27
@Contact  ：king.songtao@gmail.com
"""
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_test_email():
    from_name = "King Songtao"
    from_address = "daisongtao88@qq.com"
    from_pwd = "dgwpwdbefbjwbdjj"
    to_address = "david.songtao@hotmail.com"
    my_title = "Test Email"
    my_msg = "This is a test email."

    msg = MIMEText(my_msg, "plain", "utf-8")
    msg['From'] = formataddr([from_name, from_address])
    msg['To'] = to_address
    msg['Subject'] = my_title

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(from_address, from_pwd)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


send_test_email()
