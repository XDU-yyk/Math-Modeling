# 04 - A题参考论文pdf(1).pdf

> 自动抽取草稿：由 pypdf 文本层生成，需人工复核。

## 元数据
- 原始文件：`A题参考论文pdf(1).pdf`
- 页数：30
- 可抽取字符数：42859
- 文本缓存：`extracted-text/04-f9ac8238.txt`

## 摘要线索
本文针对 2026 年第十六届 MathorCup 数学应用挑战赛 A 题提出的带时间窗约束的车 辆路径规划问题（VRPTW） ，建立了多层次数学优化模型，综合运用精确求解与元启 发式算法，系统地解决了四个递进式子问题。 针对问题一，建立了以最小化总行驶时间为目标的混合整数线性规划（ MILP）模 型，包含客户访问唯一性约束、车辆容量约束、时间窗约束和时间连续性约束。采用 Solomon I1 插入启发式生成初始可行解，再通过 2-opt 和 Relocate 局部搜索进行改进。 最终求得最优方案使用 9 辆车，总行驶时间为 129 个时间单位，所有 50 个客户节点的 时间窗约束和容量约束均严格满足。 针对问题二，构建了两阶段层次优化模型：第一阶段以最小化车辆使用数为目标， 第二阶段在固定车辆数下最小化总行驶时间。 引入自适应大邻域搜索 （ALNS） 算法， 设 计了随机移除、最差移除两种破坏算子和贪心插入、Regret-2 插入两种修复算子，采用 模拟退火接受准则。经过 5000 次迭代，ALNS 在保持 9 辆车的前提下将总行驶时间从 129 降至 92 个时间单位，改善幅度达 28.7%。 针对问题三，将硬时间窗约束放松为软时间窗，引入迟到惩罚系数 α，建立了行驶 时间与惩罚成本的双目标优化模型。采用遗传算法（ GA）结合局部搜索进行求解，通 过对 α ∈ {0.5,

## 关键词线索
：车辆路径规划；时间窗约束；混合整数线性规划；自适应大邻域搜索；遗传算 法；灵敏度分析

## 方法关键词统计
- 灵敏度: 21
- 优化: 14
- 残差: 11
- 规划: 8
- 蒙特卡洛: 6
- 遗传算法: 5
- 评价: 4
- 模拟退火: 2
- 线性规划: 2
- 回归: 1
- 图神经网络: 1
- 热力图: 1
- 神经网络: 1
- 聚类: 1

## 标题/结构线索
- 2026 年第十六届 MathorCup 数学应用挑战赛
- 129 降至 92 个时间单位，改善幅度达 28.7%。
- 针对问题四，从车辆容量、时间窗宽度、需求波动和客户数量四个维度开展灵敏度
- 关键词：车辆路径规划；时间窗约束；混合整数线性规划；自适应大邻域搜索；遗传算
- 法；灵敏度分析
- 一 问题重述 5
- 1.1 问题背景 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
- 1.2 问题概述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
- 二 模型假设 5
- 三 符号说明 6
- 四 问题一的建模与求解 6
- 4.1 问题分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
- 4.2 数学模型 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
- 4.2.1 目标函数 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
- 4.2.2 约束条件 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
- 4.3.1 Solomon I1 插入启发式 . . . . . . . . . . . . . . . . . . . . . . . 10
- 4.3.2 局部搜索改进 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
- 4.4.1 最优路线方案 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
- 4.4.2 方法对比 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
- 五 问题二的建模与求解 14
- 5.2.1 第一阶段：最小化车辆数 . . . . . . . . . . . . . . . . . . . . . . 14
- 5.2.2 第二阶段：固定车辆数下最小化总行驶时间 . . . . . . . . . . . . 14
- 5.3 自适应大邻域搜索算法 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
- 5.3.1 破坏算子 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
- 5.3.2 修复算子 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
- 5.3.3 接受准则与自适应权重 . . . . . . . . . . . . . . . . . . . . . . . 15
- 5.3.4 算法参数 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
- 5.4.1 最优路线方案 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
- 5.4.2 方法对比分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
- 六 问题三的建模与求解 17
- 6.2.1 软时间窗定义 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
- 6.2.2 目标函数 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.2.3 约束条件 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.3 遗传算法设计 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.3.1 编码与解码 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.3.2 遗传算子 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.3.3 局部搜索嵌入 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.4.1 Pareto 前沿分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
- 6.4.2 时间窗违反分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
- 6.4.3 推荐方案 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
- 七 问题四的建模与求解 21
- 7.2 车辆容量灵敏度分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
- 7.3 时间窗宽度灵敏度分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
- 7.4 蒙特卡洛模拟分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
- 7.5 客户数量影响分析 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
- 7.6 综合灵敏度排序 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
- 八 灵敏度分析与模型检验 24
- 8.1.1 可行性验证 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
- 8.1.2 回代检验 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
- 8.1.3 交叉验证与下界分析 . . . . . . . . . . . . . . . . . . . . . . . . . 24

## 前三页片段
```text
2026 年第十六届 MathorCup 数学应用挑战赛
队伍编号
选择题号 A
带时间窗约束的车辆路径规划问题
建模与优化研究
摘 要
本文针对 2026 年第十六届 MathorCup 数学应用挑战赛 A 题提出的带时间窗约束的车
辆路径规划问题（VRPTW） ，建立了多层次数学优化模型，综合运用精确求解与元启
发式算法，系统地解决了四个递进式子问题。
针对问题一，建立了以最小化总行驶时间为目标的混合整数线性规划（ MILP）模
型，包含客户访问唯一性约束、车辆容量约束、时间窗约束和时间连续性约束。采用
Solomon I1 插入启发式生成初始可行解，再通过 2-opt 和 Relocate 局部搜索进行改进。
最终求得最优方案使用 9 辆车，总行驶时间为 129 个时间单位，所有 50 个客户节点的
时间窗约束和容量约束均严格满足。
针对问题二，构建了两阶段层次优化模型：第一阶段以最小化车辆使用数为目标，
第二阶段在固定车辆数下最小化总行驶时间。 引入自适应大邻域搜索 （ALNS） 算法， 设
计了随机移除、最差移除两种破坏算子和贪心插入、Regret-2 插入两种修复算子，采用
模拟退火接受准则。经过 5000 次迭代，ALNS 在保持 9 辆车的前提下将总行驶时间从
129 降至 92 个时间单位，改善幅度达 28.7%。
针对问题三，将硬时间窗约束放松为软时间窗，引入迟到惩罚系数 α，建立了行驶
时间与惩罚成本的双目标优化模型。采用遗传算法（ GA）结合局部搜索进行求解，通
过对 α ∈ {0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0} 进行参数扫描，生成了 Pareto 前沿。结果表
明，当 α = 0 .5 时总成本最低为 277.0，此时仅需 5 辆车，行驶时间为 127.0，但有 22
个节点存在时间窗违反。
针对问题四，从车辆容量、时间窗宽度、需求波动和客户数量四个维度开展灵敏度
分析。参数扫描结果表明，Q ≥ 40 后车辆数和行驶时间趋于稳定，Q = 35 为经济容量
拐点；时间窗缩放因子 γ = 1 .2 时总行驶时间最低（114.0） 。200 次蒙特卡洛模拟显示
方案鲁棒性良好，总行驶时间的变异系数仅为 5.85%，95% 置信区间为 [102, 129]。
关键词：车辆路径规划；时间窗约束；混合整数线性规划；自适应大邻域搜索；遗传算
法；灵敏度分析

2026 年第十六届 MathorCup 数学应用挑战赛
Abstract
This paper addresses the Vehicle Routing Problem with Time Windows (VRPTW) pro-
posed in Problem A of the 16th MathorCup Mathematical Application Challenge 2026.
We develop a multi-level mathematical optimization framework and systematically solve
four progressive sub-problems using a combination of exact methods and metaheuristic
algorithms.
For Problem 1, we formulate a Mixed-Integer Linear Programming (MILP) model
minimizing total travel time subject to customer visit uniqueness, vehicle capacity, time
window, and temporal continuity constraints. The Solomon I1 insertion heuristic gen-
erates an initial feasible solution, which is then improved via 2-opt and Relocate local
search. The optimal solution employs 9 vehicles with a total travel time of 129 time units,
satisfying all constraints for 50 customer nodes.
For Problem 2, we construct a two-phase hierarchical optimization model: Phase 1
minimizes the number of vehicles, and Phase 2 minimizes total travel time under the fixed
vehicle count. An Adaptive Large Neighborhood Search (ALNS) algorithm is designed
with random removal and worst removal destroy operators, greedy insertion and Regret-2
repair operators, and a simulated annealing acceptance criterion. After 5,000 iterations,
ALNS reduces the total travel time from 129 to 92 time units (a 28.7% improvement)
while maintaining 9 vehicles.
For Problem 3, hard time windows are relaxed to soft time windows with a late
penalty coeﬀicient α, forming a bi-objective optimization model balancing travel time and
penalty cost. A Genetic Algorithm (GA) with local search is employed, and parameter
sweeping over α ∈ { 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0} generates the Pareto front. At α =
0.5, the minimum total cost is 277.0 with only 5 vehicles, a travel time of 127.0, and 22
nodes violating time windows.
For Problem 4, sensitivity analysis is conducted across four dimensions: vehicle
capacity, time window width, demand fluctuation, and customer count. Results show
that vehicle count and travel time stabilize when Q ≥ 40, with Q = 35 as the economic
capacity threshold. The optimal time window scaling factor is γ = 1 .2 (travel time
114.0). Monte Carlo simulation (200 runs) confirms solution robustness with a coeﬀicient
of variation of only 5.85% and a 95% confidence interval of [102, 129].
Keywords: Vehicle Routing Problem; Time Windows; Mixed-Integer Linear Program-
ming; Adaptive Large Neighborhood Search; Genetic Algorithm; Sensitivity Analysis
2

2026 年第十六届 MathorCup 数学应用挑战赛
目录
一 问题重述 5
1.1 问题背景 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.2 问题概述 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
二 模型假设 5
三 符号说明 6
四 问题一的建模与求解 6
4.1 问题分析 . 
```