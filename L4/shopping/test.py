import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

'''
def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
'''
filename = "/Users/nialmajeed/Library/CloudStorage/OneDrive-Deloitte(O365D)/Documents/Projects/AI Course/AI/L4/shopping/shopping.csv"
df = pd.read_csv(filename)
Months = [
    ("Jan", "0"),
    ("Feb", "1"),
    ("Mar", "2"),
    ("Apr", "3"),
    ("May", "4"),
    ("June", "5"),
    ("Jul", "6"),
    ("Aug", "7"),
    ("Sep", "8"),
    ("Oct", "9"),
    ("Nov", "10"),
    ("Dec", "11"),
]

for Month in Months:
    df["Month"] = df["Month"].str.replace(Month[0], Month[1])
df["Month"] = df["Month"].astype("Int64")


df["VisitorType"] = df["VisitorType"].apply(
    lambda x: 1 if x == "Returning_Visitor" else 0
)
df["VisitorType"] = df["VisitorType"].astype("Int64")


df["Weekend"] = df["Weekend"].apply(lambda x: 1 if x == True else 0)
df["Weekend"] = df["Weekend"].astype("Int64")


# creating labels list from Revenue column
labels = df["Revenue"].apply(lambda x: 1 if x == True else 0)
labels = labels.values.tolist()
print(labels[0])
# creating a list from each row
# first we remove reveunue column
df1 = df.drop("Revenue", axis=1)
# now we turn the dataframe into a list of lists
evidence = df1.values.tolist()

tuple_evidence = tuple([l1, l2] for l2 in labels for l1 in evidence)

print(evidence[0])
types = df.dtypes
print(types)
