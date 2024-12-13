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

# Load HTML template from file
def load_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    return Template(template_content)

# Generate HTML and CSS for a page using LangChain
def generate_page_with_llm(page_name, description, template):
    # Define the prompt template with the loaded HTML template
    prompt_template = PromptTemplate(
        input_variables=["page_name", "description"],
        template="""
        请根据页面功能描述和模版去生成相对应的静态页面html。
        注意，根据页面功能描述去定义页面的结构、菜单和模块，生成的页面应该包含模块和模块的样例数据， 样例数据不能低于五条，且必须契合实际情况。
        请根据模版的样式和结构去生成页面，应该有菜单。
        css等样式必须和模版保持一致！
        页面名称: {page_name}
        页面功能概述: {description}
        以下是模版，注意其中的列表和内容都是需要改的，模版只是提供一个整体的样式:
        {{ template }}
        Page Name: {page_name}
        Description: {description}
        Requirements: The page should be responsive and styled for a professional B2B platform.
        """
    )

    # Set up the LangChain LLMChain
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)  # Use GPT-4 for better results
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Generate the content
    response = chain.run(page_name=page_name, description=description, template=template.render())
    return response

# Save the generated HTML and CSS files
def save_page_files(output_dir, page_name, content):
    page_dir = os.path.join(output_dir, page_name.replace(' ', '_'))
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(content)

# Main function to process the Excel file and generate pages
def main(file_path, output_dir, template_path):
    os.makedirs(output_dir, exist_ok=True)

    # Load the data
    data = load_function_data(file_path)

    # Load the HTML template
    template = load_template(template_path)

    # Generate the first page only
    first_row = data.iloc[1]
    page_name = first_row['功能页面']
    description = first_row['功能概述']

    print(f"Generating page: {page_name}")
    page_content = generate_page_with_llm(page_name, description, template)
    save_page_files(output_dir, page_name, page_content)

    print(f"Page '{page_name}' generated in {output_dir}")

if __name__ == "__main__":
    file_path = "/Users/liangxiuliang/Desktop/生成文档/功能列表/20241129-功能列表生成/基于机器学习的数据智能分析系统实施项目功能/功能清单.xlsx"
    output_dir = "./pages_generated"
    template_path = './templates/template.html'
    main(file_path, output_dir, template_path)