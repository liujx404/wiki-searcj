# -*- coding: utf-8 -*-
# @Time : 2024/1/14 21:03
# @Author : Wang Kai
# @contact: 306178200@qq.com
# @File : searcher.py
# @Software: PyCharm
import faiss
import numpy as np
from transformers import BertTokenizer, BertModel

class Searcher:
    def __init__(self, index_path, mapping_path, model_name='uer/roberta-base-finetuned-chinanews-chinese'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.index = faiss.read_index(index_path)
        self.urls = self.load_url_mapping(mapping_path)

    def load_url_mapping(self, mapping_path):
        with open(mapping_path, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file]
        return urls

    def query_to_vector(self, query):
        inputs = self.tokenizer(query, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = self.model(**inputs)
        vector = outputs.pooler_output.detach().numpy()
        return vector

    def search(self, query, k=10):
        query_vector = self.query_to_vector(query)
        _, I = self.index.search(query_vector, k)
        results = [self.urls[i] for i in I[0]]  # 根据索引找到对应的URL
        return results

if __name__=="__main__":
    # 示例用法
    searcher = Searcher('./data/wiki_zh.index', './data/wiki_map.txt')
    search_results = searcher.search('孙悟空', k=5)
    for url in search_results:
        print(url)
