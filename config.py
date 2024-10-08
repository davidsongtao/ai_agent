"""
Description: 整体项目全局配置文件，用于配置全局参数
    
-*- Encoding: UTF-8 -*-
@File     ：config.py
@Author   ：King Songtao
@Time     ：2024/10/8 上午10:21
@Contact  ：king.songtao@gmail.com
"""


class ParametersConfig(object):
    """全局参数配置"""

    def __init__(self):
        self.log_directory = r"D:\ai_agent\logs"  # 日志文件保存路径
        self.openai_api_key = "your_api_key"  # openai的API key
        self.chatglm_api_key = "your_api_key"
        self.openai_base_url = "https://api.openai.com/v1/"
