# 收集整理完成的技术规范书目录，以方便结算

import os

def list_last_segments_of_subdirectories(directory_path, output_file):
    # 确保输出文件存在，如果不存在则创建
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            pass  # 创建空文件

    # 遍历目录中的所有文件和子目录
    with open(output_file, 'a') as f:  # 使用追加模式打开文件
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isdir(full_path):  # 检查是否为目录
                last_segment = os.path.basename(full_path)  # 获取目录名称的最后一部分
                f.write(last_segment + '\n') 

if __name__ == "__main__":
    directory_path = "/Users/liangxiuliang/Desktop/生成文档/功能列表-20241209/20241209"
    output_file = "功能列表进度_20241210.txt"
    list_last_segments_of_subdirectories(directory_path, output_file)