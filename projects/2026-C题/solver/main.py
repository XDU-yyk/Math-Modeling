# -*- coding: utf-8 -*-
"""
主入口脚本
运行全部 4 个问题的求解与可视化
"""
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# 将项目根目录加入路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from solver.data_loader import load_all_data, build_friend_graph, get_user_features
from solver.community_detection import q1_main
from solver.friend_recommendation import q2_main
from solver.information_diffusion import q3_main, q4_main
from solver.visualize import (plot_community_graph, plot_diffusion_history,
                              plot_influence_ranking, plot_community_comparison,
                              plot_overlap_heatmap)

import matplotlib
matplotlib.use('Agg')  # 非交互模式


def ensure_dirs():
    """确保输出目录存在"""
    for d in ['figures', 'logs']:
        os.makedirs(os.path.join(ROOT_DIR, d), exist_ok=True)


def main():
    print("=" * 60)
    print("2026 西电数模校内赛 C题 - 完整求解")
    print("=" * 60)

    ensure_dirs()

    # 加载数据
    print("\n[Step 0] 加载数据...")
    data_dir = os.path.join(ROOT_DIR, 'data')
    friend_df, attr_df, behavior_df = load_all_data(data_dir)
    G = build_friend_graph(friend_df)
    attr_map, behavior_map = get_user_features(attr_df, behavior_df)
    print(f"  图: {G.number_of_nodes()} 节点, {G.number_of_edges()} 条边")

    # Q1: 社群发现
    print("\n[Step 1] 社群发现 (Q1)...")
    community_info = q1_main(G, attr_map, behavior_map)

    # 可视化 Q1
    print("\n[Step 1-可视化]...")
    plot_community_graph(G, community_info['partition'],
                         community_info['top_communities'],
                         save_path=os.path.join(ROOT_DIR, 'figures', 'community.png'))
    plot_community_comparison(community_info['top_communities'], behavior_map,
                              save_path=os.path.join(ROOT_DIR, 'figures', 'community_comparison.png'))
    plot_overlap_heatmap(
        [f"社群{c['comm_id']}" for c in community_info['top_communities']],
        community_info['overlap_matrix'],
        save_path=os.path.join(ROOT_DIR, 'figures', 'overlap_heatmap.png')
    )

    # Q2: 好友推荐
    print("\n[Step 2] 好友推荐 (Q2)...")
    candidates = q2_main(G, attr_map, behavior_map, target_user='S11')

    # Q3: 信息传播
    print("\n[Step 3] 信息传播与关键用户 (Q3)...")
    q3_result = q3_main(G, behavior_map)

    # 可视化 Q3
    print("\n[Step 3-可视化]...")
    plot_influence_ranking(q3_result['ranked'], top_n=20,
                           save_path=os.path.join(ROOT_DIR, 'figures', 'influence_ranking.png'))
    plot_diffusion_history(
        [q3_result['history']],
        [f"关键用户 {q3_result['key_user']} (科技类)"],
        save_path=os.path.join(ROOT_DIR, 'figures', 'diffusion.png')
    )

    # Q4: 精准推送（选做）
    print("\n[Step 4] 精准推送策略 (Q4 选做)...")
    q4_result = q4_main(G, behavior_map, community_info)

    print("\n" + "=" * 60)
    print("全部求解完成！结果文件:")
    print(f"  数据: data/")
    print(f"  代码: solver/")
    print(f"  图表: figures/")
    print(f"  日志: logs/")
    print("=" * 60)


if __name__ == '__main__':
    main()
