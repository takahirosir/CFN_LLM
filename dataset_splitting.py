from sklearn.model_selection import train_test_split

# Define the features and target variable
X = ...
y = ...

# Split the dataset into training and evaluation sets using stratified sampling
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y)
