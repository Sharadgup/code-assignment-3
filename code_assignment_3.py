# -*- coding: utf-8 -*-
"""code assignment 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D782RUyuPzwV_C68o-WlyLmxCMwhjfp4

Implement the decision tree using Python based on information gain
for splitting nodes (features). The data and information gain formula

# 1. Import Necessary Libraries:
"""

import pandas as pd
from math import log2

"""# 2. Load the Data:"""

import pandas as pd

# Data from the image (replace with actual values)
data = {
    "age": ["<=30", "<=30", "31-40", "240", ">40", ">40", "31-40", "<=30", "<=30", "40", "<=30", "31-40", "31-40", ">40"],
    "income": ["high", "high", "high", "medium", "low", "low", "low", "medium", "low", "medium", "medium", "medium", "high", "medium"],
    "student": ["no", "no", "no", "no", "yes", "yes", "yes", "no", "yes", "yes", "yes", "no", "yes", "no"],
    "credit rating": ["fair", "excellent", "fair", "fair", "fair", "excellent", "excellent", "fair", "fair", "fair", "excellent", "excellent", "fair", "excellent"],
    "buys computer": ["no", "no", "yes", "yes", "yes", "no", "yes", "no", "yes", "yes", "yes", "yes", "yes", "no"]
}

# Create DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("decision_tree_data.csv", index=False)

data = pd.read_csv('/content/decision_tree_data.csv')

data.head()

# @title age vs income

from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
plt.subplots(figsize=(8, 8))
df_2dhist = pd.DataFrame({
    x_label: grp['income'].value_counts()
    for x_label, grp in data.groupby('age')
})
sns.heatmap(df_2dhist, cmap='viridis')
plt.xlabel('age')
_ = plt.ylabel('income')

# @title income vs student

from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
plt.subplots(figsize=(8, 8))
df_2dhist = pd.DataFrame({
    x_label: grp['student'].value_counts()
    for x_label, grp in data.groupby('income')
})
sns.heatmap(df_2dhist, cmap='viridis')
plt.xlabel('income')
_ = plt.ylabel('student')

"""# 3. Define Entropy Function:"""

def entropy(S):
    if len(S) == 0:
        return 0
    pos_count = len(S[S['class'] == '+'])
    neg_count = len(S[S['class'] == '-'])
    total = pos_count + neg_count
    p_pos = pos_count / total
    p_neg = neg_count / total
    if p_pos == 0 or p_neg == 0:
        return 0
    return -p_pos * log2(p_pos) - p_neg * log2(p_neg)

"""# 4. Define Information Gain Function:"""

def information_gain(S, A):
    S_v = S.groupby(A)
    weighted_entropy = 0
    for value, subset in S_v:
        weight = len(subset) / len(S)
        weighted_entropy += weight * entropy(subset)
    return entropy(S) - weighted_entropy

"""# 5. Implement Decision Tree Construction (Pseudocode):"""

def build_tree(S, data, features, target_class="class"):
    # Base cases:
    if all(S['class'] == '+'):
        return '+'
    if all(S['class'] == '-'):
        return '-'
    if features.empty():
        return S['class'].mode()[0]  # Return majority class

    # Select best feature to split on:
    best_feature = max(features, key=lambda f: information_gain(S, f))

    # Create decision tree node:
    tree = {best_feature: {}}

    # Recursively build subtrees for each feature value:
    for value in S[best_feature].unique():
        subset = S[S[best_feature] == value]
        tree[best_feature][value] = build_tree(subset, features.drop(best_feature))

    return tree

"""# 6. Call the Functions:


"""

print(data.columns)

features = data[["age", "income", "student"]]  # Access specific columns

features = data[["age", "income", "student"]]  # Example list of features
tree = build_tree(data, features, target_class="class")  # Provide all required arguments