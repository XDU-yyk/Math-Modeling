# -*- coding: utf-8 -*-
"""
问题三：信息传播模型 - 独立级联模型
问题四（选做）：精准推送策略
"""
import numpy as np
import networkx as nx
from collections import defaultdict, Counter
import random


# 活跃时段对应的首次看到时间（距发帖的小时数）
ACTIVE_TIME_MAP = {
    '上午': 10,
    '下午': 15,
    '晚上': 20,
    '全天': 0,
}


def compute_forward_prob(user, topic, behavior_map, delta_hours,
                         alpha=0.4, beta=0.3, gamma=0.3):
    """
    计算用户转发概率

    参数:
        user: 用户 ID
        topic: 'tech' 或 'culture'
        behavior_map: 行为数据
        delta_hours: 首次看到距发帖的小时数
        alpha, beta, gamma: 权重系数
    """
    beh = behavior_map[user]

    if topic == 'tech':
        engagement = beh['tech_engagement']
    else:
        engagement = beh['culture_engagement']

    interact_freq = beh['interact_freq']

    # 参与度分量（归一化到 0-1）
    p_engage = engagement / 10.0

    # 互动频率分量（归一化，假设最高 25）
    p_freq = min(interact_freq / 25.0, 1.0)

    # 时间衰减分量（越早看到越可能转发）
    p_time = 1.0 / (1.0 + delta_hours)

    prob = alpha * p_engage + beta * p_freq + gamma * p_time
    return min(max(prob, 0.01), 0.95)  # 限制范围


def simulate_diffusion(G, source, topic, behavior_map,
                       max_hours=48, seed=42):
    """
    模拟信息传播过程 (独立级联模型)

    参数:
        G: 好友关系图
        source: 初始发帖人
        topic: 'tech' 或 'culture'
        behavior_map: 行为数据
        max_hours: 最大模拟时间（小时）
        seed: 随机种子

    返回:
        history: 每个时间点的累计感染人数
        infected_set: 最终感染用户集合
        forward_times: 每个用户转发的时间
    """
    rng = random.Random(seed)

    # 状态: 0=未看到, 1=已看到未转发, 2=已转发
    status = {node: 0 for node in G.nodes()}
    forward_time = {}  # 用户 -> 转发时间
    seen_count = defaultdict(int)  # 用户 -> 看到次数

    # 初始：发帖人立即转发
    status[source] = 2
    forward_time[source] = 0

    # 活跃队列：存储 (用户, 转发时间)
    active = [(source, 0)]

    # 记录每个时间点的感染人数
    time_points = list(range(0, max_hours + 1, 1))
    history = []

    for current_hour in range(max_hours + 1):
        # 检查当前时间点是否有新转发
        newly_forwarded = []

        for node in list(G.nodes()):
            if status[node] == 2 or status[node] == 1:
                continue  # 已转发或已处理

        # 处理从 current_hour-1 到 current_hour 之间新激活的用户
        # 检查哪些用户在这个时间点应该看到消息
        for fwd_user, fwd_time in list(active):
            if fwd_time + 1 <= current_hour <= fwd_time + 48:
                # 这个转发者的好友检查
                for neighbor in G.neighbors(fwd_user):
                    if status[neighbor] == 2:
                        continue  # 已转发

                    beh = behavior_map[neighbor]
                    active_t = beh['active_time']
                    see_hour = ACTIVE_TIME_MAP.get(active_t, 0)

                    # 检查在当前时间点是否能看到
                    # 如果当前小时等于 fwd_time + see_hour，则看到
                    if current_hour == fwd_time + see_hour and see_hour > 0:
                        # 看到消息
                        if status[neighbor] == 0:
                            status[neighbor] = 1  # 已看到
                            seen_count[neighbor] += 1

                            delta = current_hour - forward_time[fwd_user]
                            prob = compute_forward_prob(
                                neighbor, topic, behavior_map,
                                delta_hours=delta + 1
                            )

                            if rng.random() < prob:
                                status[neighbor] = 2
                                forward_time[neighbor] = current_hour
                                newly_forwarded.append(neighbor)

                    elif see_hour == 0:
                        # 全天活跃立即看到
                        prev_status = status[neighbor]
                        if status[neighbor] == 0:
                            status[neighbor] = 1
                            seen_count[neighbor] += 1

                            # 但转发概率与 fwd_time 相关
                            delta = current_hour - fwd_time + 1
                            prob = compute_forward_prob(
                                neighbor, topic, behavior_map,
                                delta_hours=delta
                            )

                            if rng.random() < prob:
                                status[neighbor] = 2
                                forward_time[neighbor] = current_hour
                                newly_forwarded.append(neighbor)

        # 更新活跃队列
        for n in newly_forwarded:
            if n not in [a[0] for a in active]:
                active.append((n, current_hour))

        # 记录累计感染人数（看到或转发）
        infected = sum(1 for s in status.values() if s > 0)
        history.append((current_hour, infected))

    infected_set = [n for n, s in status.items() if s > 0]
    return history, infected_set, forward_time


def find_key_users(G, behavior_map, topic='tech', n_simulations=30):
    """
    寻找关键用户（传播影响力最大）

    对每个用户模拟 n_simulations 次，取平均传播人数
    """
    influence_scores = {}

    for user in G.nodes():
        total_infected = 0
        for sim in range(n_simulations):
            seed = 42 + sim
            history, infected_set, _ = simulate_diffusion(
                G, user, topic, behavior_map, seed=seed
            )
            total_infected += len(infected_set)
        avg_infected = total_infected / n_simulations
        influence_scores[user] = avg_infected

        if len(influence_scores) % 50 == 0:
            print(f"  已评估 {len(influence_scores)}/{G.number_of_nodes()} 用户...")

    # 排序
    ranked = sorted(influence_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


def q3_main(G, behavior_map):
    """运行 Q3 信息传播与关键用户"""
    print("=" * 60)
    print("Q3: 信息传播与关键用户（科技类话题）")
    print("=" * 60)

    # 先找关键用户
    print("\n搜索关键用户（进行 30 次蒙特卡洛模拟取平均）...")
    ranked = find_key_users(G, behavior_map, topic='tech', n_simulations=30)

    print(f"\n传播影响力 Top 10 用户:")
    for i, (user, score) in enumerate(ranked[:10]):
        beh = behavior_map[user]
        print(f"  {i+1}. {user}: 平均传播 {score:.1f} 人"
              f" (科技参与={beh['tech_engagement']}, "
              f"互动频率={beh['interact_freq']}, "
              f"活跃时段={beh['active_time']})")

    key_user = ranked[0][0]
    print(f"\n关键用户: {key_user} (平均传播 {ranked[0][1]:.1f} 人)")

    # 模拟该关键用户 12:00 发帖后 48h 传播
    print(f"\n模拟 {key_user} 正午 12:00 发帖后 48 小时传播过程...")
    history, infected_set, forward_times = simulate_diffusion(
        G, key_user, 'tech', behavior_map, max_hours=48, seed=42
    )

    print(f"\n48 小时传播结果:")
    print(f"  最终感染人数: {len(infected_set)}")
    print(f"  传播深度（转发链路最大长度）: "
          f"{max(forward_times.values()) - min(forward_times.values()) if forward_times else 0} 小时")
    print(f"  转发用户数: {len(forward_times)}")

    # 每 6 小时输出一次传播情况
    print(f"\n传播过程（每 6 小时）:")
    print(f"{'时间(h)':>8} {'累计感染':>10}")
    for hour, count in history:
        if hour % 6 == 0:
            print(f"{hour:>8} {count:>10}")

    return {
        'key_user': key_user,
        'ranked': ranked,
        'history': history,
        'infected_set': infected_set,
        'forward_times': forward_times,
    }


def q4_main(G, behavior_map, community_info):
    """
    运行 Q4（选做）：精准推送策略

    文化类话题，每天 10 个推送名额
    """
    print("=" * 60)
    print("Q4（选做）: 精准推送策略（文化类话题）")
    print("=" * 60)

    # 使用 Q1 的社群信息 + 文化话题参与度
    top_communities = community_info['top_communities']
    partition = community_info['partition']

    # 计算每个社群的文化话题平均参与度
    comm_culture = {}
    for comm in top_communities:
        cid = comm['comm_id']
        comm_culture[cid] = {
            'avg_culture_eng': comm['avg_culture_eng'],
            'size': comm['size'],
            'members': comm['members'],
        }

    print(f"\n各社群文化话题参与度:")
    for cid, info in comm_culture.items():
        print(f"  社群 {cid}: 平均文化参与={info['avg_culture_eng']:.2f}, "
              f"规模={info['size']}人")

    # 推送策略：贪心选择
    # 每天 10 个名额，分两批推送：上午 5 个 + 下午 5 个
    # 选择文化参与度高 + 度数高（连接多）的用户

    all_users = list(G.nodes())

    # 评分：文化参与度 * (1 + 度数/avg_degree)
    degrees = dict(G.degree())
    avg_deg = np.mean(list(degrees.values()))

    user_scores = {}
    for u in all_users:
        beh = behavior_map[u]
        culture_score = beh['culture_engagement'] / 10.0
        degree_factor = 1 + degrees[u] / avg_deg
        user_scores[u] = culture_score * degree_factor

    ranked_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop 15 推荐推送用户（按文化参与×度因子）:")
    for i, (u, score) in enumerate(ranked_users[:15]):
        beh = behavior_map[u]
        time_info = beh['active_time']
        comm_id = partition.get(u, -1)
        print(f"  {i+1}. {u}: 评分={score:.3f}, "
              f"文化参与={beh['culture_engagement']}, "
              f"度={degrees[u]}, "
              f"活跃时段={time_info}, "
              f"社群={comm_id}")

    # 模拟精准推送 vs 随机推送
    print(f"\n模拟对比: 精准推送 vs 随机推送")
    print(f"（每天 10 个名额，分上午 5 个 + 下午 5 个，48 小时）")

    # 策略：选择 Top 10 推送
    push_users = [u for u, _ in ranked_users[:10]]

    # 按活跃时段分配推送
    morning_push = []
    afternoon_push = []
    for u in push_users:
        t = behavior_map[u]['active_time']
        if t == '上午' or t == '全天':
            morning_push.append(u)
        else:
            afternoon_push.append(u)

    # 调整到各 5 个
    morning_push = morning_push[:5]
    afternoon_push = afternoon_push[:5]
    # 补足
    for u in push_users:
        if len(morning_push) < 5 and u not in morning_push and u not in afternoon_push:
            morning_push.append(u)
        elif len(afternoon_push) < 5 and u not in morning_push and u not in afternoon_push:
            afternoon_push.append(u)

    print(f"\n精准推送方案:")
    print(f"  上午 10:00 推送: {morning_push}")
    print(f"  下午 15:00 推送: {afternoon_push}")

    # 模拟：对推送用户设置立即看到并转发
    def simulate_with_push(push_list, push_times, behavior_map):
        """带推送的传播模拟"""
        rng = random.Random(42)
        status = {node: 0 for node in G.nodes()}
        forward_time = {}
        active = []

        for u, t in zip(push_list, push_times):
            status[u] = 2  # 推送即转发
            forward_time[u] = t
            active.append((u, t))

        for current_hour in range(49):
            newly_fwd = []
            for fwd_user, fwd_time in list(active):
                for nb in G.neighbors(fwd_user):
                    if status[nb] == 2:
                        continue
                    beh = behavior_map[nb]
                    see_hour = ACTIVE_TIME_MAP.get(beh['active_time'], 0)
                    if current_hour == fwd_time + see_hour and see_hour > 0:
                        if status[nb] == 0:
                            status[nb] = 1
                            delta = current_hour - fwd_time
                            prob = compute_forward_prob(
                                nb, 'culture', behavior_map, delta + 1
                            )
                            if rng.random() < prob:
                                status[nb] = 2
                                forward_time[nb] = current_hour
                                newly_fwd.append(nb)
                    elif see_hour == 0:
                        if status[nb] == 0:
                            status[nb] = 1
                            delta = current_hour - fwd_time + 1
                            prob = compute_forward_prob(
                                nb, 'culture', behavior_map, delta
                            )
                            if rng.random() < prob:
                                status[nb] = 2
                                forward_time[nb] = current_hour
                                newly_fwd.append(nb)

            for n in newly_fwd:
                if n not in [a[0] for a in active]:
                    active.append((n, current_hour))

        return sum(1 for s in status.values() if s > 0)

    # 精准推送（第1天上午5个+下午5个）
    push_times = [10]*len(morning_push) + [15]*len(afternoon_push)
    push_all = morning_push + afternoon_push
    precise_result = simulate_with_push(push_all, push_times, behavior_map)

    # 随机推送
    rng = random.Random(123)
    random_users = rng.sample(all_users, 10)
    random_times = [10]*5 + [15]*5
    random_result = simulate_with_push(random_users, random_times, behavior_map)

    print(f"\n模拟结果（48 小时传播范围）:")
    print(f"  精准推送: {precise_result} 人")
    print(f"  随机推送: {random_result} 人")
    print(f"  提升比例: {(precise_result-random_result)/random_result*100:.1f}%")
    print(f"  题目参考值: 约 172 人")
    print(f"  与参考值差距: {abs(precise_result - 172) / 172 * 100:.1f}%")

    return {
        'precise_result': precise_result,
        'random_result': random_result,
        'push_users': push_all,
    }
