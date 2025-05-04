import pandas as pd
import glob
import os

def merge_csvs(input_folder, output_file):
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    dfs = []

    for file in csv_files:
        df = pd.read_csv(file)
        if 'player' not in df.columns:
            raise ValueError(f"'player' column missing in {file}")

    # Rename conflicting xg columns before merging
    for col in df.columns:
        if col != 'player' and col in [c for d in dfs for c in d.columns if c != 'player']:
        df = df.rename(columns={col: f"{col}_{os.path.basename(file).split('.')[0]}"})

        # Keep only unique columns per file
        df = df.loc[:, ~df.columns.duplicated()]

        dfs.append(df)

    # Start with first df
    merged_df = dfs[0]

    for df in dfs[1:]:
        # Drop duplicate columns from df before merge (except 'player')
        dup_cols = [col for col in df.columns if col in merged_df.columns and col != 'player']
        df = df.drop(columns=dup_cols)

        merged_df = pd.merge(merged_df, df, on='player', how='outer')

    merged_df.to_csv(output_file, index=False)
    print(f"✅ Merged CSV saved to {output_file}")

if __name__ == "__main__":
    merge_csvs("data", "merged_by_player.csv")
