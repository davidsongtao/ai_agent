"""
Description: 对main函数进行重构，使代码更加优雅
    
-*- Encoding: UTF-8 -*-
@File     ：main.py.py
@Author   ：King Songtao
@Time     ：2024/10/8 下午10:25
@Contact  ：king.songtao@gmail.com
"""
from crewai import Agent, Task, Crew, Process
from custom_tools import CustomTools
from langchain_community.chat_models import ChatZhipuAI
from log_config import *
from dotenv import load_dotenv, find_dotenv


def initialize_client():
    """初始化客户端"""
    param = ParametersConfig()
    load_dotenv(find_dotenv())
    client = ChatZhipuAI(api_key=param.chatglm_api_key, model="glm-4")
    return client


def new_agent(role, goal, backstory,  client, tools=None):
    """创建Agent代理"""
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        tools=tools or [],
        llm=client,
        allow_delegation=False
    )


def create_agents(client):
    """创建需要的三个智能体代理"""
    agents = {}
    try:
        # 创建作家代理
        agents["poet"] = new_agent(
            role="作家",
            goal="根据用户需求，创作出情感丰富的文章，确保使用中文。最长字数不过超过300个词。",
            backstory="""你作为一名著名的作家，拥有千万级别的粉丝，最擅长写情感类型的文章""",
            client=client,
        )
        logger.success(f"{agents['poet'].role}已就绪")

        # 创建编辑者代理
        agents["letter_writer"] = new_agent(
            role="内容编辑",
            goal="对作家撰写的文章内容进行精心编辑并保存到本地磁盘。",
            backstory="""作为一名经验丰富的编辑，你在编辑书信方面有多年专业经验""",
            client=client,
            tools=[CustomTools.store_poesy_to_txt]
        )
        logger.success(f"{agents['letter_writer'].role}已就绪")

        # 创建发信人代理
        agents["sender"] = new_agent(
            role="寄信人",
            goal="将编辑好的书信通过邮件发送给心仪的人",
            backstory="""你是一名勤恳的信使，专注于将书信传递给每个人""",
            client=client,
            tools=[CustomTools.send_message]
        )
        logger.success(f"{agents['sender'].role}已就绪")

        return agents
    except Exception as e:
        logger.error(f"创建智能体代理失败，错误信息：{e}")


def new_task(description, agent, output_file, expected_output):
    """创建任务"""
    return Task(
        description=description,
        agent=agent,
        output_file=output_file,
        expected_output=expected_output
    )


def create_tasks(agents):
    """创建程序要执行的三个任务，任务按照顺序执行"""
    tasks = []
    try:
        tasks.append(new_task(
            description=f"""用户需求：{input("请输入你的需求：")},
            你最后给出的答案必须是一份富含爱情表示的情书。""",
            agent=agents["poet"],
            output_file="out.txt",
            expected_output="""在这宇宙的浩瀚乐章中，你是我心弦上最动听的旋律。随着日夜更迭，我对你的情感如同不息的海浪，
            温柔而坚定地拍打着爱的海岸。我愿以星辰为笔，月光为墨，在天空中写下你的名字，让世界见证你为我的生活带来的光芒。"""
        ))
        logger.success(f"task1已就绪")

        tasks.append(new_task(
            description="""查找任何语法错误，进行编辑和格式化（如果需要）。并要求将内容保存在本地磁盘中。""",
            agent=agents["letter_writer"],
            output_file="poie.txt",
            expected_output="""在这宇宙的浩瀚乐章中，你是我心弦上最动听的旋律。随着日夜更迭，我对你的情感如同不息的海浪，
            温柔而坚定地拍打着爱的海岸。我愿以星辰为笔，月光为墨，在天空中写下你的名字。"""
        ))
        logger.success(f"task2已就绪")

        tasks.append(new_task(
            description="根据本次磁盘保存的书信内容，发送邮件给心仪的人。",
            agent=agents["sender"],
            output_file="out.txt",
            expected_output="邮件发送成功."
        ))
        logger.success(f"task3已就绪")

        return tasks
    except Exception as e:
        logger.error(f"创建任务失败，错误信息：{e}")


def create_crew(agents:dict, tasks):
    """创建crew实例并执行"""
    try:
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=2,
            process=Process.sequential
        )
        logger.success(f"crew已就绪")

        result = crew.kickoff()
        logger.success(f"任务执行完毕，结果为：{result}")
    except Exception as e:
        logger.error(f"任务执行时发生错误! 错误信息：{e}")


def main():
    """程序入口函数"""
    # 1. 初始化客户端
    client = initialize_client()
    # 2. 创建三个智能体代理
    agents = create_agents(client)
    # 3. 创建三个任务
    tasks = create_tasks(agents)
    # 4. 创建crew实例并执行任务
    create_crew(agents, tasks)


if __name__ == '__main__':
    main()
