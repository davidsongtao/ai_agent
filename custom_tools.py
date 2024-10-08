"""
Description: 自定义Tools，以供Agent使用。1.定义将Agent生成内容保存到本地文档的函数；2.定义将文本自动发送到邮箱的函数；
    
-*- Encoding: UTF-8 -*-
@File     ：custom_tools.py
@Author   ：King Songtao
@Time     ：2024/10/8 上午10:29
@Contact  ：king.songtao@gmail.com
"""
from langchain.tools import tool
from log_config import *
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib


class CustomTools:
    @tool("将文本写入文档中")
    def store_poesy_to_txt(content: str) -> str:
        """将编辑后的书信文本内容自动保存到txt文档中"""
        try:
            file_name = r"poie.txt"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(content)
            logger.success(f"将书信保存到txt文档成功！文件路径：{file_name}")
            return f"将书信保存到txt文档成功！文件路径：{file_name}"
        except Exception as e:
            logger.error(f"将书信保存到txt文档是发生错误！错误信息：{e}")
            return f"将书信保存到txt文档是发生错误！错误信息：{e}"

    @staticmethod
    @tool("发送文本到邮件")
    def send_message() -> str:
        """读取生成的本地书信文件txt文本,并以邮件的形式发送到某个人的邮箱中"""
        # 配置邮件信息
        from_name = "King Songtao"
        from_address = "daisongtao88@qq.com"
        from_pwd = "your_password"
        to_address = "fanjiang.connie@hotmail.com"
        my_title = "小情书"

        # 读取文件内容
        filename = r"poie.txt"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                my_msg = file.read()
        except Exception as e:
            logger.error(f"读取文件内容发生错误！错误信息：{e}")
            return f"读取文件内容发生错误！错误信息：{e}"

        # 配置邮件内容
        msg = MIMEText(my_msg, "plain", "utf-8")
        msg['From'] = formataddr([from_name, from_address])
        msg['Subject'] = my_title

        #  配置邮件服务器
        smtp_srv = "smtp.qq.com"

        # 发送邮件
        srv = None
        try:
            srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
            srv.login(from_address, from_pwd)
            srv.sendmail(from_address, [to_address], msg.as_string())
            logger.success(f"邮件发送成功！")
            return f"邮件发送成功！"
        except Exception as e:
            logger.error(f"邮件服务器连接失败！错误信息：{e}")
            return f"邮件服务器连接失败！错误信息：{e}"
        finally:
            if srv:
                srv.quit()
