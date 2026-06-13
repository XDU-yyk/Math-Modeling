# -*- coding: utf-8 -*-
"""
问题二：好友推荐 - 多维度相似度加权评分模型
"""
import numpy as np
import pandas as pd
from collections import Counter


def jaccard_similarity(set1, set2):
    """计算 Jaccard 相似度"""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def cosine_similarity(vec1, vec2):
    """计算余弦相似度"""
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def compute_similarity(u1, u2, attr_map, behavior_map, G):
    """计算两个用户的多维度相似度"""
    attr1, attr2 = attr_map[u1], attr_map[u2]
    beh1, beh2 = behavior_map[u1], behavior_map[u2]

    # 1. 共同好友 Jaccard 相似度 (权重 0.30)
    friends1 = set(G.neighbors(u1)) if G.has_node(u1) else set()
    friends2 = set(G.neighbors(u2)) if G.has_node(u2) else set()
    sim_friend = jaccard_similarity(friends1, friends2)

    # 2. 年级相同 (权重 0.10)
    sim_grade = 1.0 if attr1['grade'] == attr2['grade'] else 0.0

    # 3. 专业类别相同 (权重 0.15)
    sim_major_cat = 1.0 if attr1['major_cat'] == attr2['major_cat'] else 0.0

    # 4. 共同社团 (权重 0.20)
    soc1 = set(s.strip() for s in attr1['societies'] if s.strip())
    soc2 = set(s.strip() for s in attr2['societies'] if s.strip())
    sim_society = jaccard_similarity(soc1, soc2)

    # 5. 活跃时段相同 (权重 0.10)
    sim_active = 1.0 if beh1['active_time'] == beh2['active_time'] else 0.0

    # 6. 行为特征余弦相似度 (权重 0.15)
    vec1 = np.array([beh1['post_count'], beh1['interact_freq'],
                     beh1['activity_count'], beh1['tech_engagement'],
                     beh1['culture_engagement']])
    vec2 = np.array([beh2['post_count'], beh2['interact_freq'],
                     beh2['activity_count'], beh2['tech_engagement'],
                     beh2['culture_engagement']])
    sim_behavior = cosine_similarity(vec1, vec2)

    # 加权总分
    weights = {
        'friend': 0.30,
        'grade': 0.10,
        'major_cat': 0.15,
        'society': 0.20,
        'active': 0.10,
        'behavior': 0.15,
    }

    total = (weights['friend'] * sim_friend +
             weights['grade'] * sim_grade +
             weights['major_cat'] * sim_major_cat +
             weights['society'] * sim_society +
             weights['active'] * sim_active +
             weights['behavior'] * sim_behavior)

    details = {
        'friend_sim': sim_friend,
        'grade_sim': sim_grade,
        'major_cat_sim': sim_major_cat,
        'society_sim': sim_society,
        'active_sim': sim_active,
        'behavior_sim': sim_behavior,
        'total_score': total,
    }

    return total, details


def q2_main(G, attr_map, behavior_map, target_user='S11'):
    """运行 Q2 好友推荐"""
    print("=" * 60)
    print(f"Q2: 为 {target_user} 推荐好友")
    print("=" * 60)

    # 目标用户信息
    target_attr = attr_map[target_user]
    target_beh = behavior_map[target_user]
    print(f"\n目标用户 {target_user}:")
    print(f"  年级: {target_attr['grade']}")
    print(f"  专业类别: {target_attr['major_cat']}")
    print(f"  具体专业: {target_attr['major']}")
    print(f"  社团: {', '.join(target_attr['societies'])}")
    print(f"  班级: {target_attr['class']}")
    print(f"  活跃时段: {target_beh['active_time']}")
    print(f"  科技参与度: {target_beh['tech_engagement']}")
    print(f"  文化参与度: {target_beh['culture_engagement']}")

    # 已有好友
    existing_friends = set(G.neighbors(target_user)) if G.has_node(target_user) else set()
    print(f"\n已有好友数: {len(existing_friends)}")

    # 计算所有非好友用户的相似度
    candidates = []
    for user in G.nodes():
        if user != target_user and user not in existing_friends:
            score, details = compute_similarity(target_user, user, attr_map, behavior_map, G)
            candidates.append((user, score, details))

    # 按总分排序
    candidates.sort(key=lambda x: x[1], reverse=True)

    print(f"\n推荐 Top 10:")  # 先看 Top 10 再选 3
    for i, (uid, score, details) in enumerate(candidates[:10]):
        print(f"  {i+1}. {uid}: 总分={score:.4f}")
        print(f"     共同好友={details['friend_sim']:.3f}, "
              f"同年级={details['grade_sim']}, "
              f"同专业类={details['major_cat_sim']}")
        print(f"     社团重叠={details['society_sim']:.3f}, "
              f"同活跃时段={details['active_sim']}, "
              f"行为相似={details['behavior_sim']:.3f}")

    # Top 3 推荐
    top3 = candidates[:3]
    print(f"\n{'='*60}")
    print(f"推荐 Top 3:")
    for i, (uid, score, details) in enumerate(top3):
        a = attr_map[uid]
        b = behavior_map[uid]
        print(f"\n推荐 {i+1}: {uid} (总分: {score:.4f})")
        print(f"  - 年级: {a['grade']}, 专业: {a['major_cat']}/{a['major']}")
        print(f"  - 社团: {', '.join(a['societies'])}")
        print(f"  - 活跃时段: {b['active_time']}")
        print(f"  - 行为: 发布={b['post_count']}, 互动频率={b['interact_freq']}, "
              f"科技参与={b['tech_engagement']}, 文化参与={b['culture_engagement']}")

    # 分析"还不是好友"的原因
    print(f"\n{'='*60}")
    print("还不是好友的可能原因分析:")
    print(f"  {target_user} 当前已有 {len(existing_friends)} 位好友")

    # 对 Top3 分析为什么没成为好友
    for uid, score, details in candidates[:5]:
        a = attr_map[uid]
        reasons = []
        if details['friend_sim'] == 0:
            reasons.append("无共同好友")
        if details['grade_sim'] == 0:
            reasons.append(f"年级不同({target_attr['grade']} vs {a['grade']})")
        if details['major_cat_sim'] == 0:
            reasons.append(f"专业类别不同")
        if details['society_sim'] == 0:
            reasons.append("无共同社团")
        if details['active_sim'] == 0:
            reasons.append(f"活跃时段不同({target_beh['active_time']} vs {b['active_time']})")
        if details['behavior_sim'] < 0.5:
            reasons.append("行为特征差异较大")

        print(f"  {uid} (得分={score:.3f}): {'; '.join(reasons) if reasons else '多种因素综合'}")

    return candidates
