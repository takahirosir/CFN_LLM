'''
1. Data representation: 
The first step is to represent the initial status of the task set using fixed-length vectors. 
This can be done by encoding the task resource requirements as numerical values and storing them in a vector.
For example, if you have a fixed number of possible network resource requirements, you can assign a unique index to each requirement and use that index to store the corresponding value in the vector.
'''

import numpy as np

# Define the task resource requirements
# 定义任务资源需求
# processing_time代表任务处理时间
# communication_cost代表通信成本
task = {'processing_time': 10, 'communication_cost': 5}

# Define the indices for each requirement
# 定义每个需求的索引
indices = {'processing_time': 0, 'communication_cost': 1}

# Create a fixed-length vector to represent the task
# 创建一个固定长度的向量
vector = np.zeros(32)

# Encode the task resource requirements in the vector
# 在向量中编码任务资源需求
# 循环遍历task
for requirement, value in task.items():
    index = indices[requirement] # 获取对应的索引0或者1
    vector[index] = value   # 赋值
