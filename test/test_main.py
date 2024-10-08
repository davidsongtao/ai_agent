"""
Description: 单元测试脚本，用来测试main.py
    
-*- Encoding: UTF-8 -*-
@File     ：test_main.py.py
@Author   ：King Songtao
@Time     ：2024/10/8 下午11:08
@Contact  ：king.songtao@gmail.com
"""
import unittest
from unittest.mock import patch, MagicMock
from main import (
    initialize_client,
    new_agent,
    create_agents,
    new_task,
    create_tasks,
    create_crew,
    main
)


class TestMainFunctions(unittest.TestCase):

    @patch('main.load_dotenv')
    @patch('main.ChatZhipuAI')
    def test_initialize_client(self, mock_chat, mock_load_dotenv):
        mock_param = MagicMock()
        mock_param.chatglm_api_key = 'test_api_key'
        mock_chat.return_value = mock_param
        client = initialize_client()
        self.assertIsNotNone(client)
        mock_load_dotenv.assert_called_once()

    @patch('main.Agent')
    def test_new_agent(self, mock_agent):
        role = "作家"
        goal = "写一篇文章"
        backstory = "你是一名作家"
        client = MagicMock()

        agent = new_agent(role, goal, backstory, client)
        mock_agent.assert_called_once_with(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            tools=[],
            llm=client,
            allow_delegation=False
        )
        # 使用 `agent` 的 `role` 属性
        mock_agent.return_value.role = role  # 模拟返回值
        self.assertEqual(agent.role, role)

    @patch('main.new_agent')
    def test_create_agents(self, mock_new_agent):
        client = MagicMock()
        mock_new_agent.side_effect = [
            MagicMock(role="作家"),
            MagicMock(role="内容编辑"),
            MagicMock(role="寄信人")
        ]

        agents = create_agents(client)
        self.assertEqual(len(agents), 3)
        self.assertIn("poet", agents)
        self.assertIn("letter_writer", agents)
        self.assertIn("sender", agents)

    @patch('main.Task')
    def test_new_task(self, mock_task):
        description = "测试任务"
        agent = MagicMock()
        output_file = "test_output.txt"
        expected_output = "测试输出"

        task = new_task(description, agent, output_file, expected_output)
        mock_task.assert_called_once_with(
            description=description,
            agent=agent,
            output_file=output_file,
            expected_output=expected_output
        )
        # 模拟返回值
        mock_task.return_value.description = description
        self.assertEqual(task.description, description)

    @patch('main.new_task')
    def test_create_tasks(self, mock_new_task):
        agents = {
            "poet": MagicMock(),
            "letter_writer": MagicMock(),
            "sender": MagicMock()
        }
        mock_new_task.side_effect = [
            MagicMock(description="task1"),
            MagicMock(description="task2"),
            MagicMock(description="task3")
        ]

        tasks = create_tasks(agents)
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].description, "task1")
        self.assertEqual(tasks[1].description, "task2")
        self.assertEqual(tasks[2].description, "task3")

    from unittest.mock import patch, MagicMock

    @patch('main.Crew')  # 确保正确替换为您实际模块的路径
    @patch('main.Process')  # 同样确保替换为您实际模块的路径
    def test_create_crew(self, mock_process, mock_crew):
        # 设置 Process.sequential 的返回值为 MagicMock
        mock_process.sequential = MagicMock(name='sequential')

        agents = {
            "poet": MagicMock(),
            "letter_writer": MagicMock(),
            "sender": MagicMock()
        }
        tasks = [MagicMock(), MagicMock(), MagicMock()]

        crew_instance = MagicMock()
        mock_crew.return_value = crew_instance  # 确保 mock_crew 返回模拟实例

        create_crew(agents, tasks)

        # 验证 Crew 的调用
        mock_crew.assert_called_once_with(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=2,
            process=mock_process.sequential  # 使用 MagicMock
        )
        crew_instance.kickoff.assert_called_once()  # 验证 kickoff 方法被调用

    @patch('main.create_agents')
    @patch('main.create_tasks')
    @patch('main.create_crew')
    def test_main_function(self, mock_create_crew, mock_create_tasks, mock_create_agents):
        mock_create_agents.return_value = {'agent1': MagicMock()}
        mock_create_tasks.return_value = [MagicMock()]

        main()

        mock_create_agents.assert_called_once()
        mock_create_tasks.assert_called_once()
        mock_create_crew.assert_called_once()


if __name__ == '__main__':
    unittest.main()
