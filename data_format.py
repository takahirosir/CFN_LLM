import pandas as pd

# Create a sample dataset
data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
df = pd.DataFrame(data)

# Save the dataset as a CSV file
df.to_csv('data.csv', index=False)
