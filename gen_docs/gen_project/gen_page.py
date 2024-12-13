import os
from jinja2 import Template
import pandas as pd
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

# Load data from Excel file
def load_function_data(file_path):
    data = pd.read_excel(file_path)
    data.fillna(method='ffill', inplace=True)  # Fill missing values for modules and functions
    return data

# Generate HTML and CSS for a page using LangChain
def generate_page_with_llm(page_name, description):
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["page_name", "description"],
        template="""
        Create an HTML and CSS template for a web page.
        Page Name: {page_name}
        Description: {description}
        Requirements: The page should be responsive and styled for a professional B2B platform.
        """
    )

    # Set up the LangChain LLMChain
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)  # Use GPT-4 for better results
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Generate the content
    response = chain.run(page_name=page_name, description=description)
    return response

# Save the generated HTML and CSS files
def save_page_files(output_dir, page_name, content):
    page_dir = os.path.join(output_dir, page_name.replace(' ', '_'))
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(content)

# Main function to process the Excel file and generate pages
def main(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    data = load_function_data(file_path)

    # Generate the first page only
    first_row = data.iloc[0]
    page_name = first_row['功能页面']
    description = first_row['功能概述']

    print(f"Generating page: {page_name}")
    page_content = generate_page_with_llm(page_name, description)
    save_page_files(output_dir, page_name, page_content)

    print(f"Page '{page_name}' generated in {output_dir}")

if __name__ == "__main__":
    file_path = "/Users/liangxiuliang/Desktop/生成文档/功能列表/20241129-功能列表生成/基于机器学习的数据智能分析系统实施项目功能/功能清单.xlsx"
    output_dir = "./generated_pages"
    main(file_path, output_dir)
