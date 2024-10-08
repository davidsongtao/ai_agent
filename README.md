## 基于CrewAI和AI Agent技术实现情书自动撰写并通过邮件发送🚀
本次项目以 CrewAI为框架，开发 AI Agent实现自动写书信以及发送邮件。
CrewAI是一个创新的多角色agent框架，专为角色扮演中的AI代理提供自动化设置。它通过促进AI代理之间的合作，使得这些代理能够共同解决复杂问题。

### 项目基本流程
用户输入问题：帮我写一份情书 -> 写情书Task -> 作家Agent -> 编辑书信Task -> 编辑者Agent -> 寄信Task -> 寄信者Agent -> 得到邮件内容

### 环境配置
1. 安装Python环境，建议使用Anaconda。Python == 3.10
2. 安装全部依赖: pip install crewai==0.41.0; pip install langchain;
3. 使用任何大模型API需要获取对应的API Key，并配置在环境变量中。
4. 使用到的库请查看requirements.txt。

### 代码实现
1. 构建脚本custom_tools.py。定义将Agent生成内容保存到本地文档的函数；定义将文本自动发送到邮箱的函数；
2. 构建脚本main.py。定义不同角色的Agent，并设计不同任务，完成主体功能开发；

### 思考与总结
实现过程碰到很多问题，大多为版本依赖问题，调整各库版本，找到最适合的版本后，问题基本解决。