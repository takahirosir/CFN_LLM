'''
增加了一个virtualnode 解决了无解的情况
'''
import random
from gurobipy import *

class ComputingPowerNetwork():
    def __init__(self, 
                 nodes: list, 
                 processing_capabilities: dict, 
                 storage_capabilities: dict):
        self.nodes = nodes
        self.processing_capabilities = processing_capabilities
        self.storage_capabilities = storage_capabilities


class TaskList():
    def __init__(self, tasks: list, 
                 task_storage: dict, 
                 task_processing: dict,
                 data_volumes: dict, 
                 max_delays: dict):
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

    all_nodes = CPN.nodes + ["Virtual"]

    x = m.addVars(all_nodes, task_list.tasks, vtype=GRB.BINARY, name="x")
    slack = m.addVars(task_list.tasks, vtype=GRB.CONTINUOUS, name="slack")

    transmission_rates["Virtual"] = 1e-6

    m.setObjective(quicksum(task_list.data_volumes[t] / transmission_rates[n] * x[n, t] for n in all_nodes for t in task_list.tasks) + 1e3 * quicksum(slack.values()), GRB.MINIMIZE)

    for t in task_list.tasks:
        m.addConstr(quicksum(x[n, t] for n in all_nodes) == 1, name=f"task_assigned_{t}")

    for n in CPN.nodes:
        m.addConstr(quicksum(task_list.task_storage[t] * x[n, t] for t in task_list.tasks) <= CPN.storage_capabilities[n], name=f"storage_capacity_{n}")
        m.addConstr(quicksum(task_list.task_processing[t] * x[n, t] for t in task_list.tasks) <= CPN.processing_capabilities[n], name=f"processing_capacity_{n}")

    for t in task_list.tasks:
        m.addConstr(quicksum(task_list.data_volumes[t] / transmission_rates[n] * x[n, t] + task_list.task_processing[t] * x[n, t] / CPN.processing_capabilities[n] for n in all_nodes) <= task_list.max_delays[t] + slack[t], name=f"delay_{t}")

    m.optimize()

    return m

# Testing
for i in range(10):
    num_nodes = random.randint(1, 5)
    num_tasks = random.randint(num_nodes, num_nodes+5)

    nodes = [f"N_{j}" for j in range(num_nodes)]
    tasks = [f"T_{j}" for j in range(num_tasks)]

    processing_capabilities = {node: random.randint(1, 10) for node in nodes}
    storage_capabilities = {node: random.randint(10, 20) for node in nodes}
    task_storage = {task: random.randint(1, max(storage_capabilities.values())) for task in tasks}
    task_processing = {task: random.randint(1, max(processing_capabilities.values())) for task in tasks}
    data_volumes = {task: random.randint(10, 100) for task in tasks}
    max_delays = {task: random.randint(20, 50) for task in tasks}

    CPN = ComputingPowerNetwork(
        nodes=nodes,
        processing_capabilities={**processing_capabilities, "Virtual": 1e6},
        storage_capabilities={**storage_capabilities, "Virtual": 1e6}
    )

    task_list = TaskList(
        tasks=tasks,
        task_storage=task_storage,
        task_processing=task_processing,
        data_volumes=data_volumes,
        max_delays=max_delays
    )

    transmission_rates = {node: random.randint(10, 20) for node in nodes}
    m = CPN_Optimization(
        CPN=CPN,
        task_list=task_list,
        transmission_rates=transmission_rates)

    print(f"Test {i+1}")
    for v in m.getVars():
        print(f"{v.varName}: {int(v.x)}")
    print(f"Optimal schedule length: {m.objVal}\n")
