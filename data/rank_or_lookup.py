import pandas as pd

def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df = df.loc[:, ~df.columns.str.contains(r'\.\d+$')]  # remove .1, .2 suffixes
    return df

def player_lookup(df):
    player_name = input("\nEnter player name (or 'exit' to quit): ").strip()
    if player_name.lower() == 'exit':
        return
    player_row = df[df['player'].astype(str).str.contains(player_name, case=False, na=False)]
    if player_row.empty:
        print(f"❌ Player '{player_name}' not found.\n")
    else:
        print(f"\nStats for {player_name}:")
        print(player_row.to_string(index=False))

def stat_ranking(df, top_n=10):
    print("\nAvailable columns:")
    for col in df.columns:
        print(col)
    stat_column = input("\nEnter the stat column to rank players by (or 'exit' to quit): ").strip()
    if stat_column.lower() == 'exit':
        return
    if stat_column not in df.columns:
        print(f"❌ Column '{stat_column}' not found.\n")
        return
    ranked_df = df[['player', stat_column]].dropna()
    ranked_df = ranked_df.sort_values(by=stat_column, ascending=False).head(top_n)
    print(f"\nTop {top_n} players for {stat_column}:")
    print(ranked_df.to_string(index=False))

def main():
    csv_file = "merged_by_player.csv"
    df = load_data(csv_file)

    while True:
        mode = input("\nSelect mode: [1] Player lookup, [2] Stat ranking, [exit] Quit → ").strip()
        if mode == '1':
            player_lookup(df)
        elif mode == '2':
            stat_ranking(df)
        elif mode.lower() == 'exit':
            break
        else:
            print("❌ Invalid option. Please choose 1, 2, or 'exit'.")

if __name__ == "__main__":
    main()
