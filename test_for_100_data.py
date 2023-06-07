'''
此代码会造成无解情况
'''
from gurobipy import *
import random

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

# Generate 10 sets of nodes and tasks with varying quantities
for i in range(1, 11):
    num_nodes = random.randint(3, 10)
    num_tasks = random.randint(5, 15)

    nodes = [f"N{j}" for j in range(1, num_nodes+1)]
    tasks = [f"T{k}" for k in range(1, num_tasks+1)]

    processing_capabilities = {node: random.randint(10, 50) for node in nodes}
    storage_capabilities = {node: random.randint(100, 500) for node in nodes}

    CPN = ComputingPowerNetwork(
        nodes=nodes,
        processing_capabilities=processing_capabilities,
        storage_capabilities=storage_capabilities
    )

    task_storage = {task: random.randint(20, 100) for task in tasks}
    task_processing = {task: random.randint(5, 30) for task in tasks}
    data_volumes = {task: random.randint(50, 200) for task in tasks}
    max_delays = {task: random.randint(10, 40) for task in tasks}

    task_list = TaskList(
        tasks=tasks,
        task_storage=task_storage,
        task_processing=task_processing,
        data_volumes=data_volumes,
        max_delays=max_delays
    )

    transmission_rates = {node: random.randint(5, 20) for node in nodes}

    m = CPN_Optimization(
        CPN=CPN,
        task_list=task_list,
        transmission_rates=transmission_rates
    )

    # Print results
    print(f"\nResults for Set {i}:\n")
    for v in m.getVars():
        print(f"{v.varName}: {round(v.x)}")
    print(f"Optimal schedule length: {m.objVal}")
