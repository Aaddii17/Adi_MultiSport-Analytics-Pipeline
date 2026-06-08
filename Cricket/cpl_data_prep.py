import os
import pandas as pd
import csv

def prep_cpl_data(input_dir, output_file):
    print("🌴 Starting CPL ETL Pipeline...")
    all_match_dfs = []
    
    # Get all unique match IDs by looking at the file names
    files = os.listdir(input_dir)
    match_ids = set()
    for f in files:
        if f.endswith('.csv'):
            # Extracts '635215' from '635215_info.csv' or '635215.csv'
            match_ids.add(f.split('_')[0].split('.')[0])
            
    count = 0
    for mid in match_ids:
        ball_file = os.path.join(input_dir, f"{mid}.csv")
        info_file = os.path.join(input_dir, f"{mid}_info.csv")
        
        # Skip if a match is missing one of its paired files
        if not os.path.exists(ball_file) or not os.path.exists(info_file):
            continue
            
        # --- 1. Extract Metadata from the Info File ---
        match_won_by = "Unknown"
        player_of_match = "Unknown"
        
        with open(info_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[0] == 'info':
                    if row[1] == 'winner': match_won_by = row[2]
                    elif row[1] == 'player_of_match': player_of_match = row[2]
        
        # --- 2. Extract and Transform the Ball File ---
        try:
            df = pd.read_csv(ball_file)
        except Exception as e:
            print(f"Skipping {mid} due to read error: {e}")
            continue
            
        # Rename columns to perfectly match our IPL/SA20 standard schema
        rename_map = {
            'start_date': 'date',
            'runs_off_bat': 'runs_batter',
            'extras': 'runs_extras',
            'wicket_type': 'wicket_kind',
            'player_dismissed': 'player_out',
            'striker': 'batter'
        }
        df.rename(columns=rename_map, inplace=True)
        
        # Add the missing metadata to every ball in this match
        df['match_won_by'] = match_won_by
        df['player_of_match'] = player_of_match
        
        # Standardize the output to only keep what we need for the dashboard
        cols_to_keep = ['match_id', 'season', 'date', 'venue', 'match_won_by', 'player_of_match',
                        'batting_team', 'bowling_team', 'batter', 'bowler', 
                        'runs_batter', 'runs_extras', 'wicket_kind', 'player_out']
        
        # Ensure all required columns exist (fill with None if a weird file is missing one)
        for col in cols_to_keep:
            if col not in df.columns:
                df[col] = None

        # Append this clean match to our master list
        all_match_dfs.append(df[cols_to_keep])
        count += 1
        
    # Combine all 400+ matches into one massive dataframe
    print("Merging data... This might take a few seconds.")
    final_df = pd.concat(all_match_dfs, ignore_index=True)
    
    # Save the final product
    final_df.to_csv(output_file, index=False)
    print(f"✅ CPL ETL Complete! Successfully processed {count} matches.")
    print(f"📊 Total deliveries processed: {len(final_df):,}")

if __name__ == "__main__":
    INPUT_DIR = "data/CPL_Raw"
    OUTPUT_FILE = "data/cpl_combined.csv"
    prep_cpl_data(INPUT_DIR, OUTPUT_FILE)