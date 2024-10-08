"""
Description: 定义不同角色的Agent，并设计不同任务，完成主体功能开发
    
-*- Encoding: UTF-8 -*-
@File     ：main.py
@Author   ：King Songtao
@Time     ：2024/10/8 上午11:38
@Contact  ：king.songtao@gmail.com
"""
import os
from crewai import Agent, Task, Crew, Process
from custom_tools import CustomTools
from langchain_community.chat_models import ChatZhipuAI
from log_config import *
from dotenv import load_dotenv, find_dotenv

# 实例化全局参数配置
param = ParametersConfig()
_ = load_dotenv(find_dotenv())

# 实例化大模型客户端
client = ChatZhipuAI(api_key=param.chatglm_api_key, model="glm-4")
# client = ChatOpenAI(model_name="gpt-3.5-turbo", api_key="vjHZ6I8WCQqcGASGDrhfT3BlbkFJugCM9jxRSqZuKN9U9Z22")

# 定义不同的agent以及给他们的角色和目标
try:
    """作家Agent"""
    poet = Agent(
        role="作家",  # 应当表明主要功能
        goal="根据用户需求，创作出情感丰富的文章，确保使用中文。最长字数不过超过300个词。",
        backstory="""你作为一名著名的作家，拥有千万级别的粉丝，最擅长写情感类型的文章""",
        verbose=True,  # 这里设置为True, 可以打印出每一步的输入输出，方便调试
        allow_delegation=False,  # 是否允许代理，这里设置为False，表示不允许代理，直接使用大模型生成结果
        llm=client
    )
    logger.success(f"{poet.role}已就绪")
except Exception as e:
    logger.error(f"实例化poet时发生错误!错误信息：{e}")

try:
    """内容编辑"""
    letter_writer = Agent(
        role="内容编辑",
        goal="对作家撰写的文章内容及逆行精心编辑",
        backstory="""作为一名经验丰富的编辑，你在编辑书信方面有多年专业经验，
        你需要将作家写的文章内容整理编排成书信的样式，确保始终使用中文。并将书信内容存储在本地磁盘上，
        你必须使用提供的工具将书信存储到指定的文件中。请注意只保存书信内容，不要保存其他多余的话。
        """,
        verbose=True,
        allow_delegation=False,
        tools=[CustomTools.store_poesy_to_txt],
        llm=client
    )
    logger.success(f"{letter_writer.role}已就绪")
except Exception as e:
    logger.error(f"实例化letter_writer时发生错误!错误信息：{e}")

try:
    """寄信人"""
    sender = Agent(
        role="寄信人",
        goal="将编辑好的书信已邮件的形式发送给心仪的人",
        backstory="""你是一名勤恳的信使，专注于将书信传递给每个人，
        你必须使用提供的工具将指定文件的书信内容传送到其他人的邮箱里。注意，只发送书信内容，不要发送任何多余的话。
        """,
        verbose=True,
        tools=[CustomTools.send_message],
        llm=client,
        allow_delegation=False,
    )
    logger.success(f"{sender.role}已就绪")
except Exception as e:
    logger.error(f"实例化sender时发生错误!错误信息：{e}")

# 获取用户输入的需求
content = input("请输入你的需求：\n")

try:
    task1 = Task(
        description=f"""用户需求：{content},
        你最后给出的答案必须是一份富含爱情表示的情书。
        """,
        agent=poet,
        output_file=f"out.txt",
        expected_output="""在这宇宙的浩瀚乐章中，你是我心弦上最动听的旋律。随着日夜更迭，我对你的情感如同不息的海浪，
        温柔而坚定地拍打着爱的海岸。我愿以星辰为笔，月光为墨，在天空中写下你的名字，让世界见证你为我的生活带来的光芒。
        我的每一个字，都承载着我对你深深的眷恋和无尽的热爱
        """
    )
    logger.success(f"task1已就绪")
except Exception as e:
    logger.error(f"实例化task1时发生错误!错误信息：{e}")

try:
    task2 = Task(
        description="""查找任何语法错误，进行编辑和格式化（如果需要）。并要求将内容保存在本地磁盘中。将内容保存到本地非常重要，
        注意，只保存书信内容，不要保存任何多余的话。
        """,
        agent=letter_writer,
        output_file=f"poie.txt",
        expected_output="""在这宇宙的浩瀚乐章中，你是我心弦上最动听的旋律。随着日夜更迭，我对你的情感如同不息的海浪，
        温柔而坚定地拍打着爱的海岸。我愿以星辰为笔，月光为墨，在天空中写下你的名字，让世界见证你为我的生活带来的光芒。
        我的每一个字，都承载着我对你深深的眷恋和无尽的热爱
        """
    )
    logger.success(f"task2已就绪")
except Exception as e:
    logger.error(f"实例化task2时发生错误!错误信息：{e}")

try:
    task3 = Task(
        description="""根据本次磁盘保存的书信内容，你将整理并发送邮件给心仪的人，这个很重要.
        你最后的答一定要成功发送该邮件。注意，只发送书信内容，不要发送任何多余的话
        """,
        agent=sender,
        output_file=f"out.txt",
        expected_output="邮件发送成功."
    )
    logger.success(f"task3已就绪")
except Exception as e:
    logger.error(f"实例化task3时发生错误!错误信息：{e}")

# 创建一个Crew对象，并将任务添加到其中
try:
    crew = Crew(
        agents=[poet, letter_writer, sender],
        tasks=[task1, task2, task3],
        verbose=2,
        process=Process.sequential
    )
    logger.success(f"crew已就绪")
except Exception as e:
    logger.error(f"实例化crew时发生错误!错误信息：{e}")

try:
    result = crew.kickoff()
    logger.success(f"任务执行完毕，结果为：{result}")
except Exception as e:
    logger.error(f"执行任务时发生错误!错误信息：{e}")
