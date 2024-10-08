"""
Description: 
    
-*- Encoding: UTF-8 -*-
@File     ：test_openai_api.py
@Author   ：King Songtao
@Time     ：2024/10/8 下午2:47
@Contact  ：king.songtao@gmail.com
"""
import openai

# 替换为你的有效 API 密钥
openai.api_key = "your_api_key"


def test_openai_api():
    try:
        # 发送一个简单的请求来测试 API 密钥
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        # 打印返回的响应
        print("API Key is valid. Response:")
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"API Key is invalid or an error occurred: {e}")


if __name__ == "__main__":
    test_openai_api()
