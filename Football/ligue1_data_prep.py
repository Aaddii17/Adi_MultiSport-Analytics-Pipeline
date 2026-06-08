import pandas as pd
import os
import glob
import re

def extract_season(filename):
    """Extracts season from filenames like 'Ligue Season 2002 - 2003.csv' and formats to '2002/03'"""
    match = re.search(r'(\d{4})[^\d]+(\d{2,4})', filename)
    if match:
        y1 = match.group(1)
        y2 = match.group(2)
        if len(y2) == 2:
            return f"{y1}/{y2}"
        elif len(y2) == 4:
            return f"{y1}/{y2[-2:]}"
    return "Unknown"

def prep_ligue1_data(input_folder, output_file):
    print("⚽ Initializing Ligue 1 ETL Pipeline...")
    
    file_pattern = os.path.join(input_folder, "ligue1", "*.csv")
    all_files = glob.glob(file_pattern)

    if not all_files:
        print(f"⚠️ Error: No Ligue 1 files found in {input_folder}ligue1/")
        return

    df_list = []
    
    target_cols = [
        'date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr', 'hthg', 'htag', 'htr',
        'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar'
    ]

    for file in all_files:
        print(f"📥 Loading: {os.path.basename(file)}")
        
        # Handle European characters (like Saint-Étienne) and drop stray commas
        try:
            temp_df = pd.read_csv(file, encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            temp_df = pd.read_csv(file, encoding='latin-1', on_bad_lines='skip')
        
        temp_df.columns = [str(col).lower().strip() for col in temp_df.columns]
        
        rename_map = {
            'hometeam': 'home_team', 'awayteam': 'away_team'
        }
        temp_df.rename(columns=rename_map, inplace=True)
        
        temp_df['season'] = extract_season(os.path.basename(file))
        
        for col in target_cols:
            if col not in temp_df.columns:
                temp_df[col] = 0 if col not in ['ftr', 'htr', 'date', 'home_team', 'away_team'] else None
                
        if set(['home_team', 'away_team']).issubset(temp_df.columns):
            temp_df.dropna(subset=['home_team', 'away_team'], inplace=True)
            
        df_list.append(temp_df[['season'] + target_cols])

    final_df = pd.concat(df_list, ignore_index=True)

    final_df['date'] = pd.to_datetime(final_df['date'], format='mixed', dayfirst=True, errors='coerce')
    
    num_cols = ['fthg', 'ftag', 'hthg', 'htag', 'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar']
    for col in num_cols:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0).astype(int)

    final_df.to_csv(output_file, index=False)
    print(f"✅ Ligue 1 ETL Complete! Total Matches Processed: {len(final_df)}")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    OUTPUT_FILE = os.path.join(DATA_DIR, "ligue1_combined.csv")
    prep_ligue1_data(DATA_DIR, OUTPUT_FILE)