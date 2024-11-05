# 根据产品简述和产品需求分解excel,构建agent生成需求文档

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_chroma import Chroma

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "sk-QCq5pzghAUWmFHDlHYvKISaeoRP15F9y19p9VJKnmET3BlbkFJd0Ts_NtMzAaF1IRtUcbusQTPHlKpWv53rHyEoJzAkA"


class DocumentAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.chroma_db = Chroma(embedding_function=self.embeddings)
    
    
    def search_module(self, chroma_db, module_name):
        """
        在指定的色谱数据库中搜索模块。
        
        Args:
            chroma_db (ChromaDatabase): 色谱数据库对象，用于执行搜索查询。
            module_name (str): 要搜索的模块名称。
        
        Returns:
            list: 包含最多1个搜索结果的列表。
        
        """
        # Perform the search query
        results = chroma_db.similarity_search(
            query=module_name,  # Search for the module name
            k=1  # Specify the number of results to return
        )
        
        return results

    
    def process(self):

        llm = ChatOpenAI(model="gpt-4o-mini")

        # 读取产品简述, 作为之后prompt的上下文
        with open("./description.txt", 'r', encoding='utf-8') as f:
            product_description = f.read()

        # 从excel中读取产品功能，存入本地知识库，为后续RAG搭建做准备
        excel_path = "./客服会话智能分析预警系统.xlsx"
        sheets = pd.read_excel(excel_path, sheet_name=None)
        df = sheets[next(iter(sheets))]

        modules = df['模块'].unique().tolist()

        # 以模块为维度插入db
        grouped = df.groupby('模块')['功能'].apply(lambda x: ', '.join(x)).reset_index()

        # Prepare and insert into Chroma DB
        for index, row in grouped.iterrows():
            module = row['模块']
            functions = row['功能']
            # Make the content more descriptive
            doc_content = f"这是一个关于{module}模块的文档，其中功能包括: {functions}。"
            self.chroma_db.add_texts([doc_content])


        # # 查询模块相似性
        search_results = self.search_module(self.chroma_db, '语义营销分析模块')  

        # Print the search results
        for result in search_results:
            print(result)
            
if __name__ == "__main__":
    agent = DocumentAgent()
    agent.process()


    

    





    
