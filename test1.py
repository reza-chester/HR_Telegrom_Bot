import pandas as pd


df = pd.read_csv("output.csv")
final_users=df["code"].iloc[:10].tolist()
for cd in final_users:
    print(pd.isna(cd))
    print(str(cd) == 'nan' )
