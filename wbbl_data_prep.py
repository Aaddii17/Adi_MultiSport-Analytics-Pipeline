import os
import csv
import pandas as pd

def prep_wbbl_data(input_folder, output_filename):
    print(f"🦘 Adapting ETL for WBBL Format B (Split Files)...")
    all_match_dfs = []
    
    file_count = 0
    for filename in os.listdir(input_folder):
        # Only process the ball-by-ball files here, we will fetch the info file inside the loop
        if filename.endswith(".csv") and not filename.endswith("_info.csv"):
            file_count += 1
            match_id = filename.split('.')[0]
            
            ball_filepath = os.path.join(input_folder, filename)
            info_filepath = os.path.join(input_folder, f"{match_id}_info.csv")
            
            # ==========================================
            # 1. EXTRACT MATCH META-DATA
            # ==========================================
            match_won_by = 'Unknown'
            player_of_match = 'Unknown'
            
            if os.path.exists(info_filepath):
                with open(info_filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if not row or len(row) < 3: continue
                        if row[1] == 'winner': match_won_by = row[2]
                        elif row[1] == 'player_of_match': player_of_match = row[2]

            # ==========================================
            # 2. EXTRACT & MAP BALL-BY-BALL DATA
            # ==========================================
            # Since this format has headers, we can use Pandas directly!
            df = pd.read_csv(ball_filepath, low_memory=False)
            
            # Map the new Cricsheet column names back to our standard pipeline schema
            rename_map = {
                'start_date': 'date',
                'striker': 'batter',
                'runs_off_bat': 'runs_batter',
                'extras': 'runs_extras',
                'wicket_type': 'wicket_kind',
                'player_dismissed': 'player_out'
            }
            df.rename(columns=rename_map, inplace=True)
            
            # Append the metadata we extracted from the info file
            df['match_won_by'] = match_won_by
            df['player_of_match'] = player_of_match
            
            # Safety check: If a match had zero wickets, these columns might be missing
            if 'wicket_kind' not in df.columns: df['wicket_kind'] = None
            if 'player_out' not in df.columns: df['player_out'] = None
            
            # Filter down to only the columns our Match Inspector needs to save RAM
            cols_to_keep = [
                'match_id', 'date', 'season', 'venue', 'match_won_by', 'player_of_match',
                'batting_team', 'bowling_team', 'innings', 'ball', 'batter', 'non_striker',
                'bowler', 'runs_batter', 'runs_extras', 'wicket_kind', 'player_out'
            ]
            
            df = df[cols_to_keep]
            all_match_dfs.append(df)

    print("🧩 Merging all 500+ matches into master dataset...")
    final_df = pd.concat(all_match_dfs, ignore_index=True)
    final_df.to_csv(output_filename, index=False)
    print(f"✅ WBBL ETL Complete! Processed {file_count} matches seamlessly.")

if __name__ == "__main__":
    # Ensure this points to where you extracted the 1038 files
    INPUT_DIR = "data/WBBL_Raw" 
    OUTPUT_FILE = "data/wbbl_combined.csv"
    prep_wbbl_data(INPUT_DIR, OUTPUT_FILE)