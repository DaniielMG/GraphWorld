import pandas as pd

df = pd.read_csv('elestats.csv', sep=';', nrows=100000) 
df.to_csv('elestats_lite.csv', sep=';', index=False)