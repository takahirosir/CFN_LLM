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
        descfile.write('Round: Description\n')  # 添加表头

        # 运行100次
        for i in range(100):
            num_tasks = random.randint(1, 100)
            num_nodes = random.randint(1, num_tasks)  # 确保节点数不大于任务数
            tasks = np.random.randint(1, 101, size=(num_tasks, 2))
            nodes = np.random.randint(1, 101, size=(num_nodes, 1))
            max_node_power = np.max(nodes)
            tasks = np.array([task for task in tasks if task[0] <= max_node_power])

            # 生成描述并写入到描述文件中
            description = generate_description(tasks, nodes)
            descfile.write(f"{i}: {description}\n")

            # 运行K-Medoids聚类
            run_kmedoids(tasks, nodes, i, csv_writer)

# 读取并整合数据
cluster_results = {}
with open('results.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # 跳过表头
    for row in csv_reader:
        round_number = int(row[0])
        node_number = int(row[1])
        tasks = eval(row[2])
        if round_number not in cluster_results:
            cluster_results[round_number] = {}
        cluster_results[round_number][node_number] = tasks

with open('descriptions.txt', 'r') as descfile:
    lines = descfile.readlines()
    lines = lines[1:]  # 跳过表头

train_data = []
for line in lines:
    round_number, description = line.strip().split(": ", 1)
    round_number = int(round_number)

    if round_number in cluster_results:
        for node_number, tasks in cluster_results[round_number].items():
            for task_number in tasks:
                description += " 在这个设置下，第{}个任务被分配到了第{}个节点。".format(task_number + 1, node_number + 1)
    else:
        description += " 在这个设置下，无法处理任务。"

    train_data.append(description)

# 保存训练数据集
with open('training_data.txt', 'w') as f:
    for item in train_data:
        f.write("%s\n" % item)
