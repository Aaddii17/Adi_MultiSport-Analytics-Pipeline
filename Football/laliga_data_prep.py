import pandas as pd
import os
import glob
import re

def extract_season(filename):
    """If 'Season' is missing from the file, extract it from the filename."""
    match = re.search(r'(\d{4})_(\d{4})', filename)
    if match:
        return f"{match.group(1)}/{match.group(2)[-2:]}"
    return "Unknown"

def clean_season(val):
    """Formats seasons to be perfectly uniform, e.g., '1995/96'"""
    val = str(val).strip()
    if '-' in val and len(val) >= 7:
        parts = val.split('-')
        return f"{parts[0]}/{parts[1][-2:]}"
    return val

def prep_laliga_data(input_folder, output_file):
    print("⚽ Initializing La Liga ETL Pipeline...")
    file_pattern = os.path.join(input_folder, "laliga_raw*.csv")
    all_files = glob.glob(file_pattern)

    if not all_files:
        print(f"⚠️ Error: No La Liga raw files found in {input_folder}")
        return

    df_list = []
    for file in all_files:
        print(f"📥 Loading and mapping: {os.path.basename(file)}")
        df = pd.read_csv(file)

        # Smart column mapper: looks for key phrases inside messy headers
        col_map = {}
        for col in df.columns:
            c_lower = col.lower()
            if 'date' in c_lower: col_map[col] = 'date'
            elif 'season' in c_lower: col_map[col] = 'season'
            elif 'hometeam' in c_lower: col_map[col] = 'home_team'
            elif 'awayteam' in c_lower: col_map[col] = 'away_team'
            elif c_lower.startswith('fthg'): col_map[col] = 'fthg'
            elif c_lower.startswith('ftag'): col_map[col] = 'ftag'
            elif c_lower.startswith('ftr'): col_map[col] = 'ftr'

        df.rename(columns=col_map, inplace=True)

        # If older files are missing the season column, generate it
        if 'season' not in df.columns:
            df['season'] = extract_season(os.path.basename(file))

        # We only care about the columns that exist in ALL files
        common_cols = ['season', 'date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr']
        
        # Drop junk rows (like empty spaces at the bottom of CSVs)
        if set(['home_team', 'away_team']).issubset(df.columns):
            df.dropna(subset=['home_team', 'away_team'], inplace=True)

        for c in common_cols:
            if c not in df.columns:
                df[c] = None

        df_list.append(df[common_cols])

    final_df = pd.concat(df_list, ignore_index=True)

    # Standardize data types
    final_df['season'] = final_df['season'].apply(clean_season)
    final_df['fthg'] = pd.to_numeric(final_df['fthg'], errors='coerce').fillna(0).astype(int)
    final_df['ftag'] = pd.to_numeric(final_df['ftag'], errors='coerce').fillna(0).astype(int)
    final_df['date'] = pd.to_datetime(final_df['date'], format='mixed', dayfirst=True, errors='coerce')

    final_df.to_csv(output_file, index=False)
    print(f"✅ La Liga ETL Complete! Total Matches Processed: {len(final_df)}")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    OUTPUT_FILE = os.path.join(DATA_DIR, "laliga_combined.csv")
    prep_laliga_data(DATA_DIR, OUTPUT_FILE)