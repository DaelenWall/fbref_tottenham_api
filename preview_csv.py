import pandas as pd

# Load CSV
df = pd.read_csv('tottenham_dm_data.csv')

# Show first 5 rows
print(df.head())

# Show basic stats
print(df.describe())

# Show columns
print("Columns:", df.columns.tolist())
