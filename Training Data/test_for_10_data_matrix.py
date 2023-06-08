'''
增加了一个virtualnode 解决了无解的情况
'''
import random
from gurobipy import *

'''
定义一个传输网络:
Args:
    nodes: 节点列表
    processing_capabilities: 节点的处理能力
    storage_capabilities: 节点的存储能力
'''
class ComputingPowerNetwork():
    def __init__(self, 
                 nodes: list, 
                 processing_capabilities: dict, 
                 storage_capabilities: dict):
        self.nodes = nodes
        self.processing_capabilities = processing_capabilities
        self.storage_capabilities = storage_capabilities

'''
定义一个任务列表:
Args:
    tasks: 任务列表
    task_storage: 任务需要的存储空间
    task_processing: 任务需要的处理能力
    data_volumes: 任务的数据量
    max_delays: 任务的最大延迟
'''
class TaskList():
    def __init__(self, 
                 tasks: list, 
                 task_storage: dict, 
                 task_processing: dict,
                 data_volumes: dict, 
                 max_delays: dict):
        self.tasks = tasks
        self.task_storage = task_storage
        self.task_processing = task_processing
        self.data_volumes = data_volumes
        self.max_delays = max_delays

'''
定义了算力网络中的任务调度到节点的优化函数：
Args:
    CPN: 算力网络（ComputingPowerNetwork）
    task_list: 任务列表（TaskList）
    transmission_rates: 传输速率
'''
def CPN_Optimization(CPN: ComputingPowerNetwork, task_list: TaskList, transmission_rates: dict):
    # 创建一个模型
    m = Model("scheduling")
    # Disable verbose output 把日志输出关掉
    m.setParam('OutputFlag', 0)
    # Update the model to integrate new variables
    m.update()
    # 增加了一个virtualnode
    all_nodes = CPN.nodes + ["Virtual"]
    # 给模型增加变量，包括所有节点、所有任务、此变量命名为x且为二进制变量
    x = m.addVars(all_nodes, task_list.tasks, vtype=GRB.BINARY, name="x")
    # 增加松弛变量，目的是为了解决无解的情况
    slack = m.addVars(task_list.tasks, vtype=GRB.CONTINUOUS, name="slack")
    # 给Virtual节点增加传输速率
    transmission_rates["Virtual"] = 1e-6
    # 给模型增加目标函数，目标函数是最小化传输时间
    m.setObjective(quicksum(task_list.data_volumes[t] / transmission_rates[n] * x[n, t] for n in all_nodes for t in task_list.tasks) + 1e3 * quicksum(slack.values()), GRB.MINIMIZE)

    # 给模型增加约束条件，每个任务只能被分配到一个节点上
    for t in task_list.tasks:
        # quicksum是求和函数，指的是对同一个任务分配后的所有节点求和，如果等于1，说明这个任务只能被分配到一个节点上
        m.addConstr(quicksum(x[n, t] for n in all_nodes) == 1, name=f"task_assigned_{t}")

    # 给模型增加约束条件，每个节点的存储能力和处理能力都不能超过节点的最大存储能力和最大处理能力
    for n in CPN.nodes:
        # quicksum是求和函数，指的是对同一个节点分配后的所有任务求和，如果小于等于节点的最大存储能力，说明这个节点的存储能力是够的
        m.addConstr(quicksum(task_list.task_storage[t] * x[n, t] for t in task_list.tasks) <= CPN.storage_capabilities[n], name=f"storage_capacity_{n}")
        # quicksum是求和函数，指的是对同一个节点分配后的所有任务求和，如果小于等于节点的最大处理能力，说明这个节点的处理能力是够的
        m.addConstr(quicksum(task_list.task_processing[t] * x[n, t] for t in task_list.tasks) <= CPN.processing_capabilities[n], name=f"processing_capacity_{n}")

    # 给模型增加约束条件，每个任务的数据量不能超过分配到的节点的存储能力
    for t in task_list.tasks:
        # max_delays_and_slack代表每个任务处理允许的最大时延，由正常的时延要求和松弛变量组成
        max_delays_and_slack = task_list.max_delays[t] + slack[t]
        # all_nodes_delays代表每个任务分配到的所有节点的时延，由传输时延和处理时延组成
        all_nodes_delays = [task_list.data_volumes[t] / transmission_rates[n] * x[n, t] + task_list.task_processing[t] * x[n, t] / CPN.processing_capabilities[n] for n in all_nodes]
        # 限制条件，每个任务分配到的所有节点的时延不能超过允许的最大时延
        constrain = quicksum(all_nodes_delays) <= max_delays_and_slack
        # 给模型增加约束条件
        m.addConstr(constrain, name=f"delay_{t}")

    # 求解模型的最优解
    m.optimize()

    # 返回模型
    return m

# Testing
# 循环，每次随机生成一个算力网络和一个任务列表
for i in range(10):
    # 随机生成一个算力网络，具有1-5个节点
    num_nodes = random.randint(1, 5)
    # 生成节点列表，节点名称为N_0, N_1, N_2, ...
    nodes = [f"N_{j}" for j in range(num_nodes)]
    # 随机生成每个节点的处理能力，范围为1-10
    processing_capabilities = {node: random.randint(1, 10) for node in nodes}
    # 随机生成每个节点的存储能力，范围为10-20
    storage_capabilities = {node: random.randint(10, 20) for node in nodes}
    
    
    # 随机生成一个任务列表，具有比节点数量多5个以内的任务数量
    num_tasks = random.randint(num_nodes, num_nodes+5)
    # 生成任务列表，任务名称为T_0, T_1, T_2, ...
    tasks = [f"T_{j}" for j in range(num_tasks)]
    # 随机生成每个任务的存储需求，范围为1-节点存储能力的最大值之间
    task_storage = {task: random.randint(1, max(storage_capabilities.values())) for task in tasks}
    # 随机生成每个任务的处理需求，范围为1-节点处理能力的最大值之间
    task_processing = {task: random.randint(1, max(processing_capabilities.values())) for task in tasks}
    # 随机生成每个任务的数据量，范围为10-100
    data_volumes = {task: random.randint(10, 100) for task in tasks}
    # 随机生成每个任务的最大时延，范围为20-50
    max_delays = {task: random.randint(20, 50) for task in tasks}
    # 打印生成的算力网络的处理能力和存储能力
    print('processing_capabilities:',processing_capabilities,"storage_capabilities:",storage_capabilities)
    # 打印生成的任务列表的存储需求，处理需求，数据量和最大时延
    print('task_storage:',task_storage,'task_processing:',task_processing,'data_volumes:',data_volumes,'max_delays:',max_delays)

    # 实例化一个算力网络
    CPN = ComputingPowerNetwork(
        # 节点列表
        nodes=nodes,
        # 节点的处理能力，增加了一个虚拟节点，处理能力为1e6
        processing_capabilities={**processing_capabilities, "Virtual": 1e6},
        # 节点的存储能力，增加了一个虚拟节点，存储能力为1e6
        storage_capabilities={**storage_capabilities, "Virtual": 1e6}
    )

    # 实例化一个任务列表
    task_list = TaskList(
        tasks=tasks, # 任务列表
        task_storage=task_storage, # 任务的存储需求
        task_processing=task_processing, # 任务的处理需求
        data_volumes=data_volumes, # 任务的数据量
        max_delays=max_delays # 任务的最大时延
    )

    # 随机生成每个节点的传输速率，范围为10-20
    transmission_rates = {node: random.randint(10, 20) for node in nodes}
    # 实例化一个算力网络的优化器
    m = CPN_Optimization(
        CPN=CPN, # 算力网络
        task_list=task_list, # 任务列表
        transmission_rates=transmission_rates # 传输速率
        )

    # after optimization
    # 打印第几次测试循环
    print(f"Test {i+1}")

    # create an empty matrix
    # 创建一个空的矩阵，用于存储最优解
    assignment_matrix = [[0 for _ in task_list.tasks] for _ in CPN.nodes if _ != 'Virtual']

    # extract assignment matrix from model
    for v in m.getVars():
        if v.varName.startswith("x"):
            # extract node name and task name from variable name
            node_name, task_name = v.varName.split('[')[1].split(']')[0].split(',')
            # get node index and task index
            if node_name != 'Virtual':
                # 如果节点名称不是虚拟节点，则获取节点名称在节点列表中的索引
                node_index = CPN.nodes.index(node_name)
                # 获取任务名称在任务列表中的索引
                task_index = task_list.tasks.index(task_name)
                # 将最优解存储到矩阵中
                assignment_matrix[node_index][task_index] = int(v.x)

    # print matrix
    # 打印最优解矩阵
    for row in assignment_matrix:
        print(row)

    # 打印最优解的目标函数值
    print(f"Optimal schedule length: {m.objVal}\n")

    # 保存算力网络的处理能力和存储能力
    with open('processing_capabilities.txt', 'a') as f:
        f.write(str(processing_capabilities)+'\n')
    with open('storage_capabilities.txt', 'a') as f:
        f.write(str(storage_capabilities)+'\n')
    # 保存任务列表的存储需求，处理需求，数据量和最大时延
    with open('task_storage.txt', 'a') as f:
        f.write(str(task_storage)+'\n')
    with open('task_processing.txt', 'a') as f:
        f.write(str(task_processing)+'\n')
    with open('data_volumes.txt', 'a') as f:
        f.write(str(data_volumes)+'\n')
    with open('max_delays.txt', 'a') as f:
        f.write(str(max_delays)+'\n')
    # 保存最优解矩阵
    with open('assignment_matrix.txt', 'a') as f:
        f.write(str(assignment_matrix)+'\n')
        
        