import pandas as pd

df1 = pd.read_csv('library.csv')
df2 = pd.read_csv('fees.csv')

print(df1)
print(df2)

df1.loc[df1['id'] == 74, 'address'] = "Mirpur"
df1.to_csv("library.csv", index=False)