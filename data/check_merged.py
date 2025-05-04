import pandas as pd
import os

data_dir = os.path.dirname(os.path.abspath(__file__))
merged_file = os.path.join(data_dir, 'merged_by_player.csv')

df = pd.read_csv(merged_file)

print("\n📣 Columns:")
print(df.columns.tolist())

print("\n📣 First 5 rows:")
print(df.head().to_string(index=False))

