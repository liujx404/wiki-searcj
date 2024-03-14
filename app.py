# -*- coding: utf-8 -*-
# @Time : 2024/1/14 20:59
# @Author : Wang Kai
# @contact: 306178200@qq.com
# @File : app.py
# @Software: PyCharm
import streamlit as st
from searcher import Searcher

# 初始化搜索器 - 替换为你的索引和映射文件路径
searcher = Searcher('./data/wiki_zh.index', './data/wiki_map.txt')

st.title('Wiki搜索引擎')

query = st.text_input('输入你的查询', '')

if query:
    results = searcher.search(query, k=5)  # 可以调整 k 的值来改变返回的结果数量
    if results:
        st.subheader('搜索结果')
        for url in results:
            st.write(url)
    else:
        st.write('没有找到相关结果')
