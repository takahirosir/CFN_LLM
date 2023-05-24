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
# 定义数据
x = [1, 2, 3]
y = [4, 5, 6]

# Create a scatter plot
# 创建一个散点图
plt.scatter(x, y)

# Add labels and title
# 增加坐标和标题
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot')

# Show the plot
# 显示图
plt.show()
