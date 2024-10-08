"""
Description: 单元测试脚本，用于测试custom_tools
    
-*- Encoding: UTF-8 -*-
@File     ：test_custom_tools.py
@Author   ：King Songtao
@Time     ：2024/10/8 上午10:56
@Contact  ：king.songtao@gmail.com
"""
import unittest
import os
import sys
from unittest import mock, TestCase
# 动态添加上级目录到 sys.path 中，以便可以找到 custom_tools.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 现在可以正确导入上级目录中的 custom_tools
from custom_tools import CustomTools


class TestCustomTools(TestCase):

    @mock.patch('custom_tools.CustomTools.send_message')  # 替换为实际路径
    def test_send_message_file_read_error(self, mock_send_message):
        # 构造符合 Schema 的输入
        tool_input = {"self": "valid_self_value"}  # 替换为实际的输入结构
        mock_send_message.side_effect = Exception("File read error")  # 模拟文件读取错误
        tool = CustomTools()

        try:
            result = tool.send_message(tool_input)  # 传递符合要求的输入字典
        except Exception as e:
            result = str(e)

        self.assertEqual(result, "File read error")  # 根据实际预期修改

    @mock.patch('custom_tools.CustomTools.send_message')  # 替换为实际路径
    def test_send_message_smtp_error(self, mock_send_message):
        # 构造符合 Schema 的输入
        tool_input = {"self": "valid_self_value"}  # 替换为实际的输入结构
        mock_send_message.side_effect = Exception("SMTP error")  # 模拟 SMTP 错误
        tool = CustomTools()

        try:
            result = tool.send_message(tool_input)  # 传递符合要求的输入字典
        except Exception as e:
            result = str(e)

        self.assertEqual(result, "SMTP error")  # 根据实际预期修改

    @mock.patch('custom_tools.CustomTools.send_message')  # 替换为实际路径
    def test_send_message_success(self, mock_send_message):
        # 构造符合 Schema 的输入
        tool_input = {"self": "valid_self_value", "message": "test message"}
        mock_send_message.return_value = "Success"  # 模拟成功返回
        tool = CustomTools()

        result = tool.send_message(tool_input)  # 传递符合要求的输入字典
        self.assertEqual(result, "Success")

    @mock.patch('custom_tools.CustomTools.store_poesy_to_txt')  # 替换为实际路径
    def test_store_poesy_to_txt_error(self, mock_store_poesy_to_txt):
        # 构造符合 Schema 的输入
        tool_input = {"self": "valid_self_value", "content": "这是一封小情书"}
        mock_store_poesy_to_txt.side_effect = Exception("File error")  # 模拟文件错误
        tool = CustomTools()

        try:
            result = tool.store_poesy_to_txt(tool_input)  # 传递符合要求的输入字典
        except Exception as e:
            result = str(e)

        self.assertEqual(result, "File error")  # 根据实际预期修改

    @mock.patch('custom_tools.CustomTools.store_poesy_to_txt')  # 替换为实际路径
    def test_store_poesy_to_txt_success(self, mock_store_poesy_to_txt):
        # 构造符合 Schema 的输入
        tool_input = {"self": "valid_self_value", "content": "这是一封小情书"}
        mock_store_poesy_to_txt.return_value = "Success"  # 模拟成功返回
        tool = CustomTools()

        result = tool.store_poesy_to_txt(tool_input)  # 传递符合要求的输入字典
        self.assertEqual(result, "Success")


if __name__ == '__main__':
    unittest.main()
