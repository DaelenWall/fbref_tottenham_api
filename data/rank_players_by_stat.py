import pandas as pd

def rank_players(csv_file, top_n=10):
    df = pd.read_csv(csv_file)

    if 'player' not in df.columns:
        raise ValueError("'player' column not found in CSV")

    # Remove suffix columns like '.1', '.2'
    df = df.loc[:, ~df.columns.str.contains(r'\.\d+$')]

    while True:
        print("\nAvailable columns:")
        for col in df.columns:
            print(col)

        stat_column = input("\nEnter the stat column to rank players by (or 'exit' to quit): ").strip()
        if stat_column.lower() == 'exit':
            break

        if stat_column not in df.columns:
            print(f"❌ Column '{stat_column}' not found. Please try again.\n")
            continue

        # Drop NaNs and sort
        ranked_df = df[['player', stat_column]].dropna()
        ranked_df = ranked_df.sort_values(by=stat_column, ascending=False).head(top_n)

        print("\nRanking:")
        print(ranked_df.to_string(index=False))

if __name__ == "__main__":
    csv_file = "merged_by_player.csv"
    rank_players(csv_file)
