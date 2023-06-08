'''
三个计算节点
三个任务
'''
from gurobipy import *

class ComputingPowerNetwork():
    def __init__(self, nodes: list, processing_capabilities: dict, storage_capabilities: dict):
        self.nodes = nodes
        self.processing_capabilities = processing_capabilities
        self.storage_capabilities = storage_capabilities

class TaskList():
    def __init__(self, tasks: list, task_storage: dict, task_processing: dict, data_volumes: dict, max_delays: dict):
        self.tasks = tasks
        self.task_storage = task_storage
        self.task_processing = task_processing
        self.data_volumes = data_volumes
        self.max_delays = max_delays

def CPN_Optimization(CPN: ComputingPowerNetwork, task_list: TaskList, transmission_rates: dict):
    m = Model("scheduling")

    # Disable verbose output 把日志输出关掉
    m.setParam('OutputFlag', 0)
    
    m.update()

    x = m.addVars(CPN.nodes, task_list.tasks, vtype=GRB.BINARY, name="x")

    m.setObjective(quicksum(task_list.data_volumes[t] / transmission_rates[n] * x[n, t] for n in CPN.nodes for t in task_list.tasks), GRB.MINIMIZE)

    for t in task_list.tasks:
        m.addConstr(quicksum(x[n, t] for n in CPN.nodes) == 1, name=f"task_assigned_{t}")
        m.addConstr(quicksum(task_list.data_volumes[t] / CPN.processing_capabilities[n] * x[n, t] + task_list.data_volumes[t] / transmission_rates[n] * x[n, t] for n in CPN.nodes) <= task_list.max_delays[t], name=f"task_delay_{t}")

    for n in CPN.nodes:
        m.addConstr(quicksum(task_list.task_storage[t] * x[n, t] for t in task_list.tasks) <= CPN.storage_capabilities[n], name=f"node_storage_{n}")
        m.addConstr(quicksum(task_list.task_processing[t] * x[n, t] for t in task_list.tasks) <= CPN.processing_capabilities[n], name=f"node_processing_{n}")

    m.optimize()

    return m

CPN = ComputingPowerNetwork(
    nodes=['A', 'B', 'C'],
    processing_capabilities={'A': 10, 'B': 20, 'C': 30},# 添加节点计算能力
    storage_capabilities={'A': 100, 'B': 200, 'C': 300} # 添加节点存储能力
)

task_list = TaskList(
    tasks=['T1', 'T2', 'T3'],
    task_storage={'T1': 30, 'T2': 60, 'T3': 90},  # 添加任务需要的存储资源
    task_processing={'T1': 5, 'T2': 10, 'T3': 15},  # 添加任务需要的计算资源
    data_volumes={'T1': 50, 'T2': 100, 'T3': 150},  # 添加任务的数据量
    max_delays={'T1': 10, 'T2': 20, 'T3': 30}  # 添加任务允许的最大延迟
)

# 添加传输率
transmission_rates = {'A': 10, 'B': 20, 'C': 30}

m = CPN_Optimization(
    CPN=CPN,
    task_list=task_list,
    transmission_rates=transmission_rates  # 添加传输率到优化函数
)

# Print results
for v in m.getVars():
    print(f"{v.varName}: {round(v.x)}")

print(f"Optimal schedule length: {m.objVal}")
