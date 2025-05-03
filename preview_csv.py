import pandas as pd
df = pd.read_csv('tottenham_players_data.csv')
print(df.head())          # show first few rows
print(df.describe())      # summary stats
print(df.columns)         # show column names
