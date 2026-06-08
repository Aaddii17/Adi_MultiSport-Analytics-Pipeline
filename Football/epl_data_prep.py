import pandas as pd
import os
import glob

def clean_season(val):
    """Standardizes season formats (e.g., '2526', '2025-26', or '2025/26')"""
    val = str(val).strip().split('.')[0]
    if len(val) == 4 and val.isdigit():  # e.g., '2526'
        return f"20{val[:2]}/{val[2:]}"
    elif '-' in val:                     # e.g., '2025-2026'
        parts = val.split('-')
        if len(parts[0]) == 4:
            return f"{parts[0]}/{parts[1][-2:]}"
    return val

def prep_epl_data(input_folder, output_file):
    print("⚽ Initializing Advanced Premier League (EPL) ETL Pipeline...")
    
    file_pattern = os.path.join(input_folder, "epl_raw*.csv")
    all_files = glob.glob(file_pattern)
    
    if not all_files:
        print(f"⚠️ Error: Could not find any EPL raw files in {input_folder}.")
        return

    final_columns = [
        'season', 'date', 'home_team', 'away_team', 
        'fthg', 'ftag', 'ftr', 'hthg', 'htag', 'htr',
        'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar'
    ]
    
    df_list = []
    
    for file in all_files:
        print(f"📥 Processing: {os.path.basename(file)}...")
        temp_df = pd.read_csv(file)
        
        # --- FORMAT A: Team Log Style (Your new 2025/26 data) ---
        if 'opponent' in temp_df.columns and 'venue' in temp_df.columns:
            print("   -> Detected FBref Team-Log format. Parsing match perspectives...")
            
            # Filter for Home rows only to avoid counting matches twice (760 rows -> 380 unique matches)
            temp_df = temp_df[temp_df['venue'].str.lower() == 'home'].copy()
            
            processed_df = pd.DataFrame()
            processed_df['season'] = temp_df['season'].apply(clean_season)
            processed_df['date'] = temp_df['date']
            processed_df['home_team'] = temp_df['team']
            processed_df['away_team'] = temp_df['opponent']
            processed_df['fthg'] = pd.to_numeric(temp_df['GF'], errors='coerce').fillna(0).astype(int)
            processed_df['ftag'] = pd.to_numeric(temp_df['GA'], errors='coerce').fillna(0).astype(int)
            
            # Map Win/Loss/Draw from Home perspective to H/A/D
            def map_result(row):
                res = str(row['result']).upper().strip()
                if res == 'W': return 'H'
                if res == 'L': return 'A'
                return 'D'
            
            processed_df['ftr'] = temp_df.apply(map_result, axis=1)
            
            # Fill missing columns that this dataset doesn't track with 0
            for col in final_columns:
                if col not in processed_df.columns:
                    processed_df[col] = 0 if col not in ['htr'] else 'D'
            
            df_list.append(processed_df[final_columns])
            
        # --- FORMAT B: Classic Match Log Style (Your 2000-2025 data) ---
        else:
            print("   -> Detected Classic Match-Log format.")
            rename_map = {
                'Season': 'season', 'MatchDate': 'date',
                'HomeTeam': 'home_team', 'AwayTeam': 'away_team',
                'FullTimeHomeGoals': 'fthg', 'FullTimeAwayGoals': 'ftag', 'FullTimeResult': 'ftr',
                'HalfTimeHomeGoals': 'hthg', 'HalfTimeAwayGoals': 'htag', 'HalfTimeResult': 'htr',
                'HomeShots': 'hs', 'AwayShots': 'as', 'HomeShotsOnTarget': 'hst', 'AwayShotsOnTarget': 'ast',
                'HomeCorners': 'hc', 'AwayCorners': 'ac', 'HomeFouls': 'hf', 'AwayFouls': 'af',
                'HomeYellowCards': 'hy', 'AwayYellowCards': 'ay', 'HomeRedCards': 'hr', 'AwayRedCards': 'ar'
            }
            temp_df.rename(columns=rename_map, inplace=True)
            temp_df['season'] = temp_df['season'].apply(clean_season)
            
            # Ensure all required headers are present
            for col in final_columns:
                if col not in temp_df.columns:
                    temp_df[col] = 0 if col not in ['ftr', 'htr'] else 'D'
                    
            df_list.append(temp_df[final_columns])
            
    # Combine everything safely
    df = pd.concat(df_list, ignore_index=True)
    
    # Final cleanup on dates and numbers
    df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True, errors='coerce')
    num_cols = ['fthg', 'ftag', 'hthg', 'htag', 'hs', 'as', 'hst', 'ast', 'hc', 'ac', 'hf', 'af', 'hy', 'ay', 'hr', 'ar']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    df.to_csv(output_file, index=False)
    print(f"✅ Advanced EPL ETL Complete! Combined dataset saved to: {output_file}")
    print(f"📊 Total Unique Matches in Database: {len(df)}")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    OUTPUT_FILE = os.path.join(DATA_DIR, "epl_combined.csv")
    prep_epl_data(DATA_DIR, OUTPUT_FILE)