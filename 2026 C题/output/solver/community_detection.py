# -*- coding: utf-8 -*-
"""
问题一：社群发现 - Louvain 算法
"""
import networkx as nx
import pandas as pd
import numpy as np
from collections import Counter
import community as community_louvain


def detect_communities(G):
    """使用 Louvain 算法检测社区"""
    partition = community_louvain.best_partition(G)
    return partition


def get_community_density(G, community_nodes):
    """计算社群内部边密度"""
    n = len(community_nodes)
    if n <= 1:
        return 0.0
    subgraph = G.subgraph(community_nodes)
    e_in = subgraph.number_of_edges()
    max_possible = n * (n - 1) / 2
    return e_in / max_possible if max_possible > 0 else 0.0


def get_top_dense_communities(G, partition, top_k=5):
    """找出内部连接密度最大的 k 个社群"""
    # 按社群分组
    communities = {}
    for node, comm_id in partition.items():
        if comm_id not in communities:
            communities[comm_id] = []
        communities[comm_id].append(node)

    # 计算每个社群的密度
    comm_density = []
    for comm_id, nodes in communities.items():
        density = get_community_density(G, nodes)
        comm_density.append((comm_id, nodes, density))

    # 按密度排序
    comm_density.sort(key=lambda x: x[2], reverse=True)

    return comm_density[:top_k]


def analyze_communities(top_communities, attr_map, behavior_map):
    """分析社群特征画像"""
    results = []
    for comm_id, nodes, density in top_communities:
        grades = []
        major_cats = []
        societies = []
        tech_eng = []
        culture_eng = []
        active_times = []

        for node in nodes:
            if node in attr_map:
                a = attr_map[node]
                grades.append(a['grade'])
                major_cats.append(a['major_cat'])
                societies.extend(a['societies'])
            if node in behavior_map:
                b = behavior_map[node]
                tech_eng.append(b['tech_engagement'])
                culture_eng.append(b['culture_engagement'])
                active_times.append(b['active_time'])

        # 统计
        grade_dist = dict(Counter(grades))
        major_dist = dict(Counter(major_cats))
        society_dist = dict(Counter([s.strip() for s in societies if s.strip()]))
        time_dist = dict(Counter(active_times))

        results.append({
            'comm_id': comm_id,
            'size': len(nodes),
            'density': density,
            'members': sorted(nodes),
            'grade_dist': grade_dist,
            'major_dist': major_dist,
            'society_dist': society_dist,
            'active_time_dist': time_dist,
            'avg_tech_eng': np.mean(tech_eng) if tech_eng else 0,
            'avg_culture_eng': np.mean(culture_eng) if culture_eng else 0,
        })

    return results


def compute_overlap(results):
    """计算社群两两之间的重叠度（Jaccard 相似度）"""
    n = len(results)
    overlap_matrix = np.zeros((n, n))
    names = [f"社群{r['comm_id']}" for r in results]

    for i in range(n):
        set_i = set(results[i]['members'])
        for j in range(n):
            set_j = set(results[j]['members'])
            if i == j:
                overlap_matrix[i][j] = 1.0
            else:
                intersection = len(set_i & set_j)
                union = len(set_i | set_j)
                overlap_matrix[i][j] = intersection / union if union > 0 else 0.0

    return names, overlap_matrix


def q1_main(G, attr_map, behavior_map):
    """运行 Q1 社群发现"""
    print("=" * 60)
    print("Q1: 社群发现")
    print("=" * 60)

    # Louvain 社区发现
    partition = detect_communities(G)
    n_communities = len(set(partition.values()))
    modularity = community_louvain.modularity(partition, G)
    print(f"发现 {n_communities} 个社群")
    print(f"模块度 Q = {modularity:.4f}")

    # 密度最大的 5 个社群
    top5 = get_top_dense_communities(G, partition, top_k=5)

    print(f"\n密度最大的 5 个社群:")
    for i, (comm_id, nodes, density) in enumerate(top5):
        print(f"  社群 {comm_id}: 规模={len(nodes)}, 密度={density:.4f}")

    # 特征分析
    analysis = analyze_communities(top5, attr_map, behavior_map)
    for r in analysis:
        print(f"\n--- 社群 {r['comm_id']} 特征 ---")
        print(f"  成员: {', '.join(r['members'][:10])}{'...' if r['size']>10 else ''}")
        print(f"  年级分布: {r['grade_dist']}")
        print(f"  专业分布: {r['major_dist']}")
        print(f"  热门社团: {dict(sorted(r['society_dist'].items(), key=lambda x: x[1], reverse=True)[:5])}")
        print(f"  平均科技参与: {r['avg_tech_eng']:.2f}")
        print(f"  平均文化参与: {r['avg_culture_eng']:.2f}")

    # 重叠度分析
    names, overlap_matrix = compute_overlap(analysis)
    print(f"\n社群重叠度（Jaccard 相似度）:")
    print(f"{'':12s}", end="")
    for name in names:
        print(f"{name:10s}", end="")
    print()
    for i, name in enumerate(names):
        print(f"{name:12s}", end="")
        for j in range(len(names)):
            print(f"{overlap_matrix[i][j]:.4f}    ", end="")
        print()

    # 判断是否有重叠
    max_overlap = 0
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            max_overlap = max(max_overlap, overlap_matrix[i][j])
    if max_overlap > 0.1:
        print(f"\n结论: 社群间存在一定重叠（最大 Jaccard={max_overlap:.4f}），")
        print(f"       表现为成员共享和相似的特征分布")
    else:
        print(f"\n结论: 社群间重叠程度较低（最大 Jaccard={max_overlap:.4f}），")
        print(f"       功能定位区分明显")

    # 返回结果用于 Q4
    return {
        'partition': partition,
        'top_communities': analysis,
        'overlap_matrix': overlap_matrix,
        'modularity': modularity,
    }
