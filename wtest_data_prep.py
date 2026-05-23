import os
import csv
import pandas as pd

def prep_wtest_data(input_folder, output_filename):
    print(f"🏏 Initializing Women's Test (WTest) ETL Pipeline...")
    all_match_dfs = []
    
    file_count = 0
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv") and not filename.endswith("_info.csv"):
            file_count += 1
            match_id = filename.split('.')[0]
            
            ball_filepath = os.path.join(input_folder, filename)
            info_filepath = os.path.join(input_folder, f"{match_id}_info.csv")
            
            # ==========================================
            # 1. EXTRACT MATCH META-DATA (HANDLING DRAWS)
            # ==========================================
            match_won_by = 'Unknown'
            player_of_match = 'Unknown'
            
            if os.path.exists(info_filepath):
                with open(info_filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if not row or len(row) < 3: continue
                        if row[1] == 'winner': 
                            match_won_by = row[2]
                        elif row[1] == 'outcome' and row[2] == 'draw':
                            match_won_by = 'Draw'
                        elif row[1] == 'player_of_match': 
                            player_of_match = row[2]

            # ==========================================
            # 2. EXTRACT & MAP BALL-BY-BALL DATA
            # ==========================================
            df = pd.read_csv(ball_filepath, low_memory=False)
            
            rename_map = {
                'start_date': 'date',
                'striker': 'batter',
                'runs_off_bat': 'runs_batter',
                'extras': 'runs_extras',
                'wicket_type': 'wicket_kind',
                'player_dismissed': 'player_out'
            }
            df.rename(columns=rename_map, inplace=True)
            
            df['match_won_by'] = match_won_by
            df['player_of_match'] = player_of_match
            
            if 'wicket_kind' not in df.columns: df['wicket_kind'] = None
            if 'player_out' not in df.columns: df['player_out'] = None
            
            cols_to_keep = [
                'match_id', 'date', 'season', 'venue', 'match_won_by', 'player_of_match',
                'batting_team', 'bowling_team', 'innings', 'ball', 'batter', 'non_striker',
                'bowler', 'runs_batter', 'runs_extras', 'wicket_kind', 'player_out'
            ]
            
            cols_present = [c for c in cols_to_keep if c in df.columns]
            df = df[cols_present]
            all_match_dfs.append(df)

    print("🧩 Combining Test matches and parsing years...")
    final_df = pd.concat(all_match_dfs, ignore_index=True)
    
    final_df['date'] = pd.to_datetime(final_df['date'], format='mixed', errors='coerce')
    final_df['year'] = final_df['date'].dt.year.fillna(0).astype(int).astype(str)
    final_df['year'] = final_df['year'].replace('0', 'Unknown')
    
    final_df.to_csv(output_filename, index=False)
    print(f"✅ WTest ETL Complete! Processed {file_count} Test matches.")

if __name__ == "__main__":
    INPUT_DIR = "data/WTest_Raw" 
    OUTPUT_FILE = "data/wtest_combined.csv"
    prep_wtest_data(INPUT_DIR, OUTPUT_FILE)