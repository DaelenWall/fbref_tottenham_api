import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set data directory relative to script location
data_dir = script_dir

# List all CSV files in the directory
csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

if not csv_files:
    print("⚠️ No CSV files found in the directory!")
else:
    # Loop through each CSV file and preview
    for file in csv_files:
        file_path = os.path.join(data_dir, file)
        print(f"\n===== Preview of {file} =====")
        df = pd.read_csv(file_path)
        print(df.to_string(index=False))  # ✅ Show full DataFrame nicely
