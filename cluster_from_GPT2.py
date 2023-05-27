from pyclustering.cluster.kmedoids import kmedoids
import numpy as np
import sys
import random
import csv

# 生成描述
def generate_description(tasks, nodes):
    description = "我们有{}个节点和{}个任务。".format(len(nodes), len(tasks))

    for i, node in enumerate(nodes, 1):
        description += "第{}个节点的处理能力为{}，".format(i, node[0])

    for i, task in enumerate(tasks, 1):
        description += "第{}个任务的算力需求为{}和最大时延需求为{}，".format(i, task[0], task[1])

    description = description[:-1] + "。"
    return description

# 对每一组数据运行K-Medoids聚类
def run_kmedoids(tasks, nodes, round_number, csv_writer):
    distances = np.zeros((len(tasks), len(nodes)))

    for i, task in enumerate(tasks):
        for j, node in enumerate(nodes):
            compute_time = task[0] / max(node[0], 1e-10) 
            comm_time = task[1] / 2
            total_time = compute_time + comm_time
            if total_time > task[1]:  
                total_time = sys.maxsize
            distances[i][j] = total_time

    if len(nodes) >= 2 and len(tasks) >= len(nodes):
        initial_medoids = list(range(len(nodes)))
        kmedoids_instance = kmedoids(distances, initial_medoids)
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()

        for i, cluster in enumerate(clusters):
            csv_writer.writerow([round_number, i, cluster])

# 创建一个CSV文件
with open('results.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Round', 'Node', 'Tasks'])

    # 创建一个描述文件
    with open('descriptions.txt', 'w') as descfile:

        # 运行100次
        for i in range(100):
            num_tasks = random.randint(1, 100)
            num_nodes = random.randint(1, 100)
            tasks = np.random.randint(1, 101, size=(num_tasks, 2))
            nodes = np.random.randint(1, 101, size=(num_nodes, 1))
            max_node_power = np.max(nodes)
            tasks = np.array([task for task in tasks if task[0] <= max_node_power])

            if len(tasks) == 0:
                print(f"Round {i}: No tasks can be processed. Skipping this round.")
                continue

            # 生成描述并写入到描述文件中
            description = generate_description(tasks, nodes)
            descfile.write(f"Round {i}: {description}\n")

            # 运行K-Medoids聚类
            run_kmedoids(tasks, nodes, i, csv_writer)
