import pandas as pd
from GenTransac import TypeDepense

df = pd.read_csv("D:\\WORK\\PING\\Programming\\transactions.csv")

cid = 15634602
totals = [0,0,0,0,0,0,0,0,0,0,0]

allstats = []

for index, row in df.iterrows():
    if row['CustomerId'] != cid:
        total = 0
        for i in range(len(totals)):
            total += totals[i]
        for i in range(len(totals)):
            totals[i] /= total
        totals.insert(0, cid)
        allstats.append(totals)
        
        cid = row['CustomerId']
        totals = [0,0,0,0,0,0,0,0,0,0,0]

    td = TypeDepense[row['TransactionType'].split('.')[1]]
    totals[td.value] += row['Value']

total = 0
for i in range(len(totals)):
    total += totals[i]
for i in range(len(totals)):
    totals[i] /= total
totals.insert(0, cid)
allstats.append(totals)

df2 = pd.DataFrame.from_records(allstats, columns=["CustomerId", "ALIMENTATION", "LOISIRS", "MULTIMEDIA", "RESTAURANTS", "RETRAITS", "SANTE", "SHOPPING", "AUTRES", "LOYER", "ELECTRICITE", "INTERNET"])
df2.to_csv("D:\\WORK\\PING\\Programming\\user_stats.csv", index=False)
