import numpy as np

# Define the task resource requirements
task = {'processing_time': 10, 'communication_cost': 5}

# Define the indices for each requirement
indices = {'processing_time': 0, 'communication_cost': 1}

# Create a fixed-length vector to represent the task
vector = np.zeros(32)

# Encode the task resource requirements in the vector
for requirement, value in task.items():
    index = indices[requirement]
    vector[index] = value
