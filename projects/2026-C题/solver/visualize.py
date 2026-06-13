# -*- coding: utf-8 -*-
"""
可视化模块
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def plot_community_graph(G, partition, top5_info, save_path='figures/community.png'):
    """可视化社群图"""
    plt.figure(figsize=(14, 10))

    # 给节点着色
    top_members = set()
    for comm in top5_info:
        for m in comm['members']:
            top_members.add(m)

    colors = []
    for node in G.nodes():
        if node in top_members:
            cid = partition[node]
            # 使用颜色映射
            colors.append(cid)
        else:
            colors.append(-1)

    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    # 绘制非 Top5 社群节点（灰色小点）
    other_nodes = [n for n in G.nodes() if n not in top_members]
    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes,
                           node_color='lightgray', node_size=30, alpha=0.4)

    # 绘制 Top5 社群节点
    for comm in top5_info:
        cid = comm['comm_id']
        members = comm['members']
        nx.draw_networkx_nodes(G, pos, nodelist=members,
                               node_color=plt.cm.tab10(cid % 10),
                               node_size=80, alpha=0.9, label=f'社群{cid}')

    # 绘制边
    nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color='gray')

    # 标签
    for comm in top5_info:
        cx = np.mean([pos[m][0] for m in comm['members']])
        cy = np.mean([pos[m][1] for m in comm['members']])
        plt.text(cx, cy, f"社群{comm['comm_id']}\n({comm['size']}人, 密度={comm['density']:.3f})",
                 fontsize=10, fontweight='bold', ha='center',
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))

    plt.title('校园圈社交网络社群结构', fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"社群图已保存: {save_path}")


def plot_diffusion_history(histories, labels, save_path='figures/diffusion.png'):
    """绘制传播过程曲线"""
    plt.figure(figsize=(10, 6))

    for history, label in zip(histories, labels):
        hours = [h[0] for h in history]
        counts = [h[1] for h in history]
        plt.plot(hours, counts, label=label, linewidth=2)

    plt.xlabel('时间 (小时)', fontsize=12)
    plt.ylabel('累计感染人数', fontsize=12)
    plt.title('信息传播过程', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 48)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"传播曲线已保存: {save_path}")


def plot_influence_ranking(ranked, top_n=20, save_path='figures/influence_ranking.png'):
    """绘制关键用户影响力排名"""
    plt.figure(figsize=(12, 6))

    users = [r[0] for r in ranked[:top_n]]
    scores = [r[1] for r in ranked[:top_n]]

    colors = plt.cm.Reds(np.linspace(0.3, 0.9, top_n))
    plt.barh(range(top_n), scores, color=colors[::-1])
    plt.yticks(range(top_n), users)
    plt.xlabel('平均传播人数', fontsize=12)
    plt.title('用户传播影响力排名 (Top 20)', fontsize=14)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"影响力排名图已保存: {save_path}")


def plot_community_comparison(top5_info, behavior_map,
                              save_path='figures/community_comparison.png'):
    """对比 Top5 社群的多维特征"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    labels = [f"社群{c['comm_id']}" for c in top5_info]

    # 1. 规模对比
    sizes = [c['size'] for c in top5_info]
    axes[0].bar(labels, sizes, color=plt.cm.tab10(range(5)))
    axes[0].set_title('社群规模')
    axes[0].set_ylabel('成员数')

    # 2. 密度对比
    densities = [c['density'] for c in top5_info]
    axes[1].bar(labels, densities, color=plt.cm.tab10(range(5)))
    axes[1].set_title('内部边密度')
    axes[1].set_ylabel('密度')

    # 3. 科技参与度
    tech_avgs = [c['avg_tech_eng'] for c in top5_info]
    axes[2].bar(labels, tech_avgs, color=plt.cm.Blues(np.linspace(0.4, 0.9, 5)))
    axes[2].set_title('平均科技话题参与度')
    axes[2].set_ylabel('参与度')

    # 4. 文化参与度
    culture_avgs = [c['avg_culture_eng'] for c in top5_info]
    axes[3].bar(labels, culture_avgs, color=plt.cm.Oranges(np.linspace(0.4, 0.9, 5)))
    axes[3].set_title('平均文化话题参与度')
    axes[3].set_ylabel('参与度')

    # 5. 专业分布
    for i, c in enumerate(top5_info):
        major_dist = c['major_dist']
        axes[4].bar(i, major_dist.get('工科', 0), color='steelblue', width=0.4)
        axes[4].bar(i, major_dist.get('理科', 0), bottom=major_dist.get('工科', 0),
                     color='orange', width=0.4)
        axes[4].bar(i, major_dist.get('文科', 0),
                     bottom=major_dist.get('工科', 0) + major_dist.get('理科', 0),
                     color='green', width=0.4)
    axes[4].set_xticks(range(5))
    axes[4].set_xticklabels(labels)
    axes[4].set_title('专业分布')
    axes[4].legend(['工科', '理科', '文科'], fontsize=9)
    axes[4].set_ylabel('人数')

    # 6. 年级分布（堆叠）
    grade_colors = {'大一': '#FF9999', '大二': '#66B2FF', '大三': '#99FF99',
                    '大四': '#FFCC99', '研究生': '#CC99FF'}
    grades_list = ['大一', '大二', '大三', '大四', '研究生']
    bottom = np.zeros(5)
    for g in grades_list:
        vals = [c['grade_dist'].get(g, 0) for c in top5_info]
        axes[5].bar(range(5), vals, bottom=bottom, label=g,
                     color=grade_colors.get(g, 'gray'), width=0.6)
        bottom += vals
    axes[5].set_xticks(range(5))
    axes[5].set_xticklabels(labels)
    axes[5].set_title('年级分布')
    axes[5].legend(fontsize=8)
    axes[5].set_ylabel('人数')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"社群对比图已保存: {save_path}")


def plot_overlap_heatmap(names, overlap_matrix,
                         save_path='figures/overlap_heatmap.png'):
    """绘制社群重叠度热力图"""
    plt.figure(figsize=(8, 6))
    plt.imshow(overlap_matrix, cmap='YlOrRd', vmin=0, vmax=1, aspect='auto')

    for i in range(len(names)):
        for j in range(len(names)):
            plt.text(j, i, f'{overlap_matrix[i][j]:.3f}',
                     ha='center', va='center',
                     color='white' if overlap_matrix[i][j] > 0.5 else 'black')

    plt.xticks(range(len(names)), names, rotation=45)
    plt.yticks(range(len(names)), names)
    plt.colorbar(label='Jaccard 相似度')
    plt.title('社群重叠度热力图')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"重叠度热力图已保存: {save_path}")
