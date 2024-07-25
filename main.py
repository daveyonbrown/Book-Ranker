import pandas as pd
from collections import defaultdict

y = pd.read_csv("ratings.csv")

print(y)
ids = y["user_id"]
x = list(ids)
print(x[0])