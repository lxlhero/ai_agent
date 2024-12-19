import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import json
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
import docx
from typing import Any
import logging
from docx.shared import Pt
import traceback
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from pydantic import BaseModel, Field
import pathlib


folder = pathlib.Path(__file__).parent.resolve()
print(f'当前python文件所在目录：{folder}')

# 从环境变量中获取 OPENAI_API_KEY
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
else:
    os.environ["OPENAI_API_KEY"] = str(openai_api_key)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# class TestMethodKeyInfo(BaseModel):
#     test_range: str = Field(description="测试范围，包含具体内容")
#     function_test: str = Field(description="功能测试，包含具体内容")
#     key_function_test_case: str = Field(description="关键功能测试用例示例，每个用例包含描述、前置条件、测试步骤、预期结果")

class DataPreprocessingModuleSpecGenerator:
    def __init__(self, overview_path, feature_excel_path):
        # 初始化参数
        self.embeddings = OpenAIEmbeddings()
        self.chroma_db = Chroma(embedding_function=self.embeddings)
        self.overview_path = overview_path
        self.feature_excel_path = feature_excel_path

    def excel_to_json(self):
        # 读取上传的Excel文件
        excel_data = pd.read_excel(self.feature_excel_path)

        # 填充空白单元格，对于模块名称和功能模块列，使用向前填充的方法
        excel_data['模块'] = excel_data['模块'].fillna(method='ffill')
        excel_data['功能'] = excel_data['功能'].fillna(method='ffill')
        excel_data['功能页面'] = excel_data['功能页面'].fillna(method='ffill')

        # 创建一个空的列表来存储结果
        result = []

        # 按模块名称和功能模块分组
        for module_name, group in excel_data.groupby(['模块', '功能', '功能页面']):
            # 获取当前模块名称和功能模块
            current_module_name, current_function_module, current_function_page = module_name
            if "合计" in current_module_name:
                continue

            # 获取当前功能模块的所有详细说明
            details = group['功能概述'].tolist()

            # 将当前功能模块及其详细说明添加到结果列表中
            result.append({
                '模块': current_module_name,
                '功能': current_function_module,
                '功能页面': current_function_page,
                '功能概述': details
            })

        # 将结果列表转换为JSON格式
        json_data = pd.json_normalize(result)

        return json_data.to_json(orient='records', force_ascii=False)

    def process(self):
        temperature = 0
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        # structured_llm = self.llm.with_structured_output(TestMethodKeyInfo)

        # 读取产品简述
        with open(self.overview_path, 'r', encoding='utf8') as f:
            product_description = f.read()

        with open(f'{folder}/sample_test_method.txt', 'r', encoding='utf8') as f:
            sample_test_method = f.read()

        with open(f'{folder}/sample_test_record.txt', 'r', encoding='utf8') as f:
            sample_test_report = f.read()

        # 读取采购报价单excel
        product_details = self.excel_to_json()

        template = PromptTemplate.from_file(f"{folder}/template_prompt.txt")
        prompt = template.format(
            product_description=product_description,
            product_details=product_details,
            sample_test_method=sample_test_method,
            sample_test_report=sample_test_report
        )

        # 使用LLM生成JSON
        result = self.llm.invoke(prompt)
        print(f"llm生成: {result.content}")

        # 解析结果中测试范围、功能测试、关键功能测试用例示例
        test_range = result.content.split("# 测试范围")[1].split("# 功能测试")[0].strip()
        function_test = result.content.split("# 功能测试")[1].split("# 关键功能测试用例示例")[0].strip()
        key_function_test_case = result.content.split("# 关键功能测试用例示例")[1].strip()

        print(f"测试范围: {test_range}")
        print(f"功能测试: {function_test}")
        print(f"关键功能测试用例示例: {key_function_test_case}")

        # 读取template_test_method.txt的内容，并且将test_range、function_test、key_function_test_case替换到其中，并写入到result.md文件中
        with open(f'{folder}/template_test_method.txt', 'r', encoding='utf8') as f:
            template_test_method = f.read()
        with open(f'{folder}/result.md', 'w', encoding='utf8') as f:
            f.write(template_test_method.replace("{test_range}", test_range).replace("{function_test}", function_test).replace("{key_function_test_case}", key_function_test_case))

        # try:
        #     # Strip leading/trailing whitespace and newlines
        #     stripped_response = func_names_json_response.strip().strip('```json')

        #     # Parse the stripped response into JSON
        #     func_names_info = json.loads(stripped_response)

        #     # Use func_names_info as needed
        #     print("功能详情:", func_names_info)

        # except json.JSONDecodeError as e:
        #     # Handle JSON decoding errors
        #     print(f"JSON decoding error: {e}")
        #     func_names_info = None  # Or set to a default value

        # except Exception as e:
        #     # Handle any other unexpected errors
        #     print(f"An error occurred: {e}")
        #     func_names_info = None  # Or set to a default value
        # try:
        #     self.save_func_names_json_to_excel(func_names_info, "./功能清单.xlsx")
        #     print(f"功能清单已保存")
        # except json.JSONDecodeError as e:
        #     print(f"JSON 解码错误: {e}")
        #     func_names_json = None

if __name__ == "__main__":
    # Define the list of platforms

    # Path to the product overview
    overview_path = f"{folder}/overview.txt"
    feature_excel_path = "/Users/yangbo/projects/llm/docreator/ai_agent/featurelist/基于机器学习的民航指挥智能态势感知系统实施项目功能/功能清单.xlsx"

    generator = DataPreprocessingModuleSpecGenerator(
            overview_path=overview_path,
            feature_excel_path=feature_excel_path
        )
    try:
        generator.process()
        logger.info(f"成功生成功能清单")
    except Exception as e:
        logger.error(f"生成功能清单失败！")
        logger.error("Traceback details:", exc_info=True)