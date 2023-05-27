from pyclustering.cluster.kmedoids import kmedoids
import numpy as np
import sys
import random
import csv

# 对每一组数据运行K-Medoids聚类
def run_kmedoids(tasks, nodes, round_number, csv_writer):
    # 计算距离矩阵
    distances = np.zeros((len(tasks), len(nodes)))

    for i, task in enumerate(tasks):
        for j, node in enumerate(nodes):
            compute_time = task[0] / max(node[0], 1e-10)  # 保证不会除以0
            comm_time = task[1] / 2
            total_time = compute_time + comm_time
            if total_time > task[1]:  # 如果总时间超过任务的最大时延需求
                total_time = sys.maxsize  # 设置总时间为无穷大
            distances[i][j] = total_time

    if len(nodes) >= 2 and len(tasks) >= len(nodes):
        # 使用KMedoids算法，初始化聚类中心为节点的索引
        initial_medoids = list(range(len(nodes)))
        kmedoids_instance = kmedoids(distances, initial_medoids)

        # 对任务进行聚类
        kmedoids_instance.process()

        # 输出每个任务的标签，标签表示任务被分配到哪个节点
        clusters = kmedoids_instance.get_clusters()

        for i, cluster in enumerate(clusters):
            csv_writer.writerow([round_number, i, cluster])

# 创建一个CSV文件
with open('results.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Round', 'Node', 'Tasks'])

    # 运行100次
    for i in range(100):
        # 随机生成任务数和节点数
        num_tasks = random.randint(1, 100)
        num_nodes = random.randint(1, 100)

        # 随机生成任务和节点
        tasks = np.random.randint(1, 101, size=(num_tasks, 2))
        nodes = np.random.randint(1, 101, size=(num_nodes, 1))

        # 移除不能被任何节点处理的任务
        max_node_power = np.max(nodes)
        tasks = np.array([task for task in tasks if task[0] <= max_node_power])

        # 如果没有可处理的任务，则跳过这次循环
        if len(tasks) == 0:
            print(f"Round {i}: No tasks can be processed. Skipping this round.")
            continue

        # 运行K-Medoids聚类
        run_kmedoids(tasks, nodes, i, csv_writer)
