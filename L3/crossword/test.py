import pandas as pd

set1 = set(["s1v1", "s1v2", "s1v3"])
set2 = set(["s2v1", "s2v2", "s2v3"])

df1 = pd.DataFrame({"s1": list(set1)})
df2 = pd.DataFrame({"s2": list(set2)})
join_df = df1.merge(df2, how="cross")
# list of all arcs
all_arc = list(join_df.itertuples(index=False, name=None))

print(all_arc)
