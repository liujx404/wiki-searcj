# -*- coding: utf-8 -*-
# 指定文件编码为utf-8
# @Time : 2024/1/14 21:00
# 这是创建文件的时间
# @Author : Wang Kai
# 作者名称
# @contact: 306178200@qq.com
# 联系方式
# @File : indexer.py
# 文件名称
# @Software: PyCharm
# 使用的软件是PyCharm

import faiss  # 导入faiss用于高效相似度搜索和稠密向量聚类
import numpy as np  # 导入numpy用于数学运算
import pandas as pd  # 导入pandas进行数据处理
from tqdm import tqdm  # 从tqdm导入tqdm用于进度条显示
import torch  # 导入torch用于深度学习模型
from transformers import BertTokenizer, BertModel  # 从transformers导入预训练模型和分词器

class Indexer:  # 定义索引器类
    def __init__(self, model_name='uer/roberta-base-finetuned-chinanews-chinese', batch_size=8):  # 初始化方法
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'  # 判断是否使用CUDA
        self.tokenizer = BertTokenizer.from_pretrained(model_name)  # 加载预训练分词器
        self.model = BertModel.from_pretrained(model_name).to(self.device)  # 加载预训练模型并放到合适的设备上
        self.index = faiss.IndexFlatL2(768)  # 创建一个faiss索引，BERT的向量大小为768
        self.batch_size = batch_size  # 设置处理的批量大小
        self.url_mapping = []  # 存储每个向量对应的URL的列表

    def texts_to_vectors(self, texts):  # 定义方法，将文本转换为向量
        vectors = []  # 初始化向量列表
        for i in tqdm(range(0, len(texts), self.batch_size)):  # tqdm显示进度条
            batch_texts = texts[i:i + self.batch_size].tolist()  # 获取一批文本
            inputs = self.tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True, max_length=512)  # 使用tokenizer进行编码
            inputs = {k: v.to(self.device) for k, v in inputs.items()}  # 将所有编码后的数据移至合适的设备
            outputs = self.model(**inputs)  # 输入模型进行转换
            batch_vectors = outputs.pooler_output.detach().cpu().numpy()  # 获取向量并移至cpu
            vectors.extend(batch_vectors)  # 合并向量
        return np.array(vectors)  # 返回向量数组

    def add_to_index(self, texts, urls):  # 定义方法，将文本和对应的url加入索引
        vectors = self.texts_to_vectors(texts)  # 获得文本对应的向量
        self.index.add(vectors)  # 将向量加入faiss index
        self.url_mapping.extend(urls)  # 加入url映射

    def save_index_and_mapping(self, index_path, mapping_path):  # 定义方法，保存索引和映射
        faiss.write_index(self.index, index_path)  # 将索引保存到指定路径
        with open(mapping_path, 'w', encoding='utf-8') as f:  # 打开文件准备将url映射写入
            for url in self.url_mapping:  # 遍历url映射
                f.write(url + '\n')  # 写入url到文件

    def build_index_from_csv(self, csv_file_path):  # 定义方法，从CSV文件建立索引
        df = pd.read_csv(csv_file_path)[:1000]  # 读取CSV文件并限制为1000条数据
        self.add_to_index(df['content'], df['url'])  # 将文本内容和url添加到索引

if __name__=="__main__":  # 当文件被作为脚本运行时
    indexer = Indexer()  # 创建Indexer实例
    indexer.build_index_from_csv('./data/wiki_zh.csv')  # 从CSV文件建立索引
    indexer.save_index_and_mapping('./data/wiki_zh.index', './data/wiki_map.txt')  # 保存索引和映射
