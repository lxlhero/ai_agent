1. MetaGPT
   1. https://github.com/geekan/MetaGPT
   2. 教程: https://docs.deepwisdom.ai/main/en/guide/get_started/introduction.html
   3. 安装按照教程，python 3.11可以

2. 方法论
   1. 总的思路是先确定prompt, 后构建代码
   2. 第一步是梳理生成内容的结构， 以生成需求excel为例，输入是一个产品的简述，输出为多个模块，每个模块有多个功能，每个功能有多个功能页面，每个页面有一个概述
   3. 通过交互式gpt对话尝试生成，成功后记录prompts
   4. 梳理每次prompt获取哪几个层次上的数据，并规范gpt的输出
      1. 以excel为例，第一个prompt生成所有模块，之后每个模块只用一个prompt去获取所有详细信息，给出输出实例去规范输出：

        PROMPT_TEMPLATE: str = """
            Based on the product description: '{description}', generate a list of module.
            no other except modules should be output, and output should be Chinese
            example:
            '1. **数据摄取模块：**'， 
            2. **数据存储与管理模块：**'
            3. **数据处理与分析模块：**'
            """


        PROMPT_TEMPLATE: str = (
            """For the module '{module}', provide a detailed list of functions. For each function, include function pages and a brief function overview.
            Requirements: 
            output should be Chinese except for keywords as Module, Function, Function Page, Function Overview.
            Each module can have multiple functions.
            Each function is a name like Data source management
            Each function can have multiple function pages which is a page name like Add data source page.
            Each function page has a brief overview description like Add a data source and provide a graphical interface for users to enter basic information of the data source (such as database type, IP address, port number, user name, password, etc.) and connection parameters.
            The output should be include keywords for each item, example:
            
            Module：数据集成和预处理

            Function：数据源管理
                Function Page：添加数据源页面
                Function Overview：添加数据源，并提供图形界面供用户输入数据源的基本信息（如数据库类型、IP地址、端口号、用户名、密码）和连接参数。

                Function Page：数据源列表页面
                Function Overview：显示已添加的数据源列表，允许用户编辑、删除或测试每个数据源的连接。
                
            Function：数据清洗
                Function Page：清洗规则配置页面
                Function Overview：提供接口供用户定义各种清理规则（例如，删除空值、替换错误值、设置数据类型约束）以进行数据预处理。
            """
        )

    3. 以prompt为核心构建action及role，写代码