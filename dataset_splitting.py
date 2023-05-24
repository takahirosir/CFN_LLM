'''
3. Dataset splitting: 
The dataset can be split into training and evaluation sets using a suitable method such as stratified sampling. 
This method ensures that the proportions of different classes or categories in the training and evaluation sets are similar to those in the overall dataset.
To split the dataset into training and evaluation sets using stratified sampling in Python, you can use the train_test_split() function from the scikit-learn library. 
Here is an example that shows how to split a dataset into training and evaluation sets using stratified sampling:
'''
from sklearn.model_selection import train_test_split

# Define the features and target variable
# 定义特征变量
X = ...
y = ...

# Split the dataset into training and evaluation sets using stratified sampling
# 使用stratified sampling将数据集分成test和train两部分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y)
