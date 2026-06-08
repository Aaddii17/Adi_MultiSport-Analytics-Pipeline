import pandas as pd
import os
import glob
import numpy as np

def prep_mls_data(input_folder, output_file):
    print("⚽ Initializing MLS ETL Pipeline...")
    
    file_pattern = os.path.join(input_folder, "mls", "*.csv")
    all_files = glob.glob(file_pattern)

    if not all_files:
        print(f"⚠️ Error: No MLS files found in {input_folder}mls/")
        return

    df_list = []
    
    target_cols = [
        'season', 'date', 'home_team', 'away_team', 'fthg', 'ftag', 'ftr', 'hthg', 'htag', 'htr',
        'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar'
    ]

    for file in all_files:
        print(f"📥 Loading and mapping: {os.path.basename(file)}")
        
        try:
            temp_df = pd.read_csv(file, encoding='utf-8', on_bad_lines='skip', low_memory=False)
        except UnicodeDecodeError:
            temp_df = pd.read_csv(file, encoding='latin-1', on_bad_lines='skip', low_memory=False)
            
        temp_df.columns = [str(col).lower().strip() for col in temp_df.columns]
        
        # SCHEMA 1: 1996 - 2022 Format
        if 'home_score' in temp_df.columns:
            temp_df.rename(columns={
                'home': 'home_team', 'away': 'away_team', 
                'home_score': 'fthg', 'away_score': 'ftag', 'year': 'season'
            }, inplace=True)
            
            # Calculate FTR (Full Time Result) since it's missing in this file
            temp_df['fthg'] = pd.to_numeric(temp_df['fthg'], errors='coerce').fillna(0)
            temp_df['ftag'] = pd.to_numeric(temp_df['ftag'], errors='coerce').fillna(0)
            
            conditions = [
                (temp_df['fthg'] > temp_df['ftag']),
                (temp_df['fthg'] < temp_df['ftag'])
            ]
            temp_df['ftr'] = np.select(conditions, ['H', 'A'], default='D')

        # SCHEMA 2: 2012 - 2026 Format
        elif 'hg' in temp_df.columns or 'fthg' in temp_df.columns:
            rename_map = {
                'home': 'home_team', 'away': 'away_team', 
                'hg': 'fthg', 'ag': 'ftag', 'res': 'ftr'
            }
            temp_df.rename(columns={k: v for k, v in rename_map.items() if k in temp_df.columns}, inplace=True)
        
        # Clean up Season format (MLS is typically a single year, e.g., '2015')
        if 'season' in temp_df.columns:
            temp_df['season'] = temp_df['season'].astype(str).str[:4]
            
        # Ensure all columns exist
        for col in target_cols:
            if col not in temp_df.columns:
                temp_df[col] = 0 if col not in ['ftr', 'htr', 'date', 'home_team', 'away_team', 'season'] else None
                
        if set(['home_team', 'away_team', 'date']).issubset(temp_df.columns):
            temp_df.dropna(subset=['home_team', 'away_team', 'date'], inplace=True)
            
        df_list.append(temp_df[target_cols])

    # Combine the files
    final_df = pd.concat(df_list, ignore_index=True)

    # Standardize Dates
    final_df['date'] = pd.to_datetime(final_df['date'], format='mixed', dayfirst=False, errors='coerce')

    # DEDUPLICATION: Remove overlapping matches between the two files
    initial_len = len(final_df)
    # Sort so that rows with more advanced stats (sum of hs, as, hc, etc.) bubble to the top and are kept
    final_df['stat_sum'] = final_df[['hs', 'as', 'hc', 'ac', 'hf', 'af']].sum(axis=1)
    final_df = final_df.sort_values('stat_sum', ascending=False)
    
    final_df.drop_duplicates(subset=['date', 'home_team', 'away_team'], keep='first', inplace=True)
    final_df.drop(columns=['stat_sum'], inplace=True)
    
    print(f"🧹 Deduplication complete: Removed {initial_len - len(final_df)} duplicate matches.")

    # Convert numeric columns safely
    num_cols = ['fthg', 'ftag', 'hthg', 'htag', 'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar']
    for col in num_cols:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0).astype(int)

    final_df.to_csv(output_file, index=False)
    print(f"✅ MLS ETL Complete! Total Unique Matches Processed: {len(final_df)}")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    OUTPUT_FILE = os.path.join(DATA_DIR, "mls_combined.csv")
    prep_mls_data(DATA_DIR, OUTPUT_FILE)