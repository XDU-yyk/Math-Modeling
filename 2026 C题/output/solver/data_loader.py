# -*- coding: utf-8 -*-
"""
数据加载模块 - 加载校园圈抽样数据
"""
import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def load_all_data(data_dir=None):
    """加载所有数据表"""
    if data_dir is None:
        data_dir = DATA_DIR

    xlsx_path = None
    for f in os.listdir(data_dir):
        if f.endswith('.xlsx'):
            xlsx_path = os.path.join(data_dir, f)
            break

    if xlsx_path is None:
        raise FileNotFoundError(f"未找到 Excel 文件: {data_dir}")

    # 加载三个工作表
    friend_df = pd.read_excel(xlsx_path, sheet_name='好友关系表')
    attr_df = pd.read_excel(xlsx_path, sheet_name='用户属性表')
    behavior_df = pd.read_excel(xlsx_path, sheet_name='行为数据表')

    return friend_df, attr_df, behavior_df


def build_friend_graph(friend_df):
    """构建好友关系图"""
    import networkx as nx
    G = nx.Graph()
    for _, row in friend_df.iterrows():
        G.add_edge(row.iloc[0], row.iloc[1])
    return G


def get_user_features(attr_df, behavior_df):
    """合并用户属性与行为特征"""
    # 用户属性
    attr_map = {}
    for _, row in attr_df.iterrows():
        uid = row['学生ID']
        attr_map[uid] = {
            'grade': row.iloc[1],
            'major_cat': row.iloc[2],
            'major': row.iloc[3],
            'societies': str(row.iloc[4]).split(',') if pd.notna(row.iloc[4]) else [],
            'class': row.iloc[5],
        }

    # 行为数据
    behavior_map = {}
    for _, row in behavior_df.iterrows():
        uid = row['学生ID']
        behavior_map[uid] = {
            'post_count': row.iloc[1],
            'interact_freq': row.iloc[2],
            'activity_count': row.iloc[3],
            'tech_engagement': row.iloc[4],
            'culture_engagement': row.iloc[5],
            'active_time': row.iloc[6],
        }

    return attr_map, behavior_map


if __name__ == '__main__':
    friend_df, attr_df, behavior_df = load_all_data()
    G = build_friend_graph(friend_df)
    print(f"用户数: {G.number_of_nodes()}")
    print(f"好友关系数: {G.number_of_edges()}")
    print(f"好友关系表: {friend_df.shape}")
    print(f"用户属性表: {attr_df.shape}")
    print(f"行为数据表: {behavior_df.shape}")
