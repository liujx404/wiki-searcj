# -*- coding: utf-8 -*-
# @Time : 2024/1/14 21:20
# @Author : Wang Kai
# @contact: 306178200@qq.com
# @File : process_data.py
# @Software: PyCharm
import json
import csv
import os

def process_line_to_csv(json_line, csv_writer):
    """
    将单行JSON格式数据转换为CSV格式，并写入CSV文件
    :param json_line: 单行JSON格式的字符串
    :param csv_writer: CSV文件的写入对象
    """
    try:
        # 解析JSON格式数据
        article = json.loads(json_line)
        # 获取文章内容和URL
        content = article.get('text', '')
        url = article.get('url','')
        # 将文章内容和URL写入CSV文件
        csv_writer.writerow([content,url])
    except json.JSONDecodeError:
        # 如果解析JSON格式数据失败，则打印警告信息
        print("警告：无法解析的行")

def process_file(json_file_path, csv_writer):
    """
    读取JSON文件中的所有行，并将其转换为CSV文件
    :param json_file_path: JSON文件的路径
    :param csv_writer: CSV文件的写入对象
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        # 按行读取文件内容
        for line in file:
            # 对每一行执行JSON到CSV的转换
            process_line_to_csv(line, csv_writer)

def process_directory(directory_path, output_file, num_file = 100):
    """
    遍历指定文件夹，将所有JSON文件转换为单个CSV文件
    :param directory_path: 文件夹路径
    :param output_file: 输出CSV文件的路径
    :param num_file: 最多处理的文件数量（默认为100）
    """
    # 创建CSV文件，并打开用于写入
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入CSV的标题行
        writer.writerow(['content','url'])

        file_count = 0

        # 遍历目录中的所有文件
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_count += 1
                # 构造完整的文件路径
                json_file_path = os.path.join(root, file)
                # 处理单个JSON文件，将数据写入CSV
                process_file(json_file_path, writer)
                print(f"Iter:{file_count}/{num_file} Process File: {json_file_path}")
                # 如果处理的文件数达到指定数量，则提前结束
                if file_count > num_file:
                    return

if __name__=="__main__":
    # 指定wiki2019zh数据集的目录路径
    wiki_directory = './data/wiki_zh'
    # 指定输出CSV文件的路径
    output_csv = './data/wiki_zh.csv'
    # 指定要处理的数据文件数量
    num_file = 100
    # 执行目录处理函数
    process_directory(wiki_directory, output_csv, num_file)
