'''
2. Data formatting: 
Once the fixed-length vectors have been created, they can be used as input to the Large Language Model. 
The input sequence should consist of the vectors representing the initial status of the task set. 
These vectors can be stored in a suitable data format such as CSV.
'''
import pandas as pd

# Create a sample dataset
data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
df = pd.DataFrame(data)

# Save the dataset as a CSV file
df.to_csv('data.csv', index=False)
