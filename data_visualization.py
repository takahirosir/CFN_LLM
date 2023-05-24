'''
4. Data visualization: 
It may be useful to visualize the dataset to gain insights into its characteristics. 
This can be done by creating tables or plots that summarize the data. 
For example, a scatter plot can be used to visualize the relationship between different task resource requirements.
To create a scatter plot in Python, you can use libraries such as Matplotlib or Seaborn. 
These libraries provide easy-to-use interfaces for creating various types of plots and charts. 
Here is an example that shows how to create a scatter plot using Matplotlib:
'''
import matplotlib.pyplot as plt

# Define the data
x = [1, 2, 3]
y = [4, 5, 6]

# Create a scatter plot
plt.scatter(x, y)

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot')

# Show the plot
plt.show()
