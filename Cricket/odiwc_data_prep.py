import os
import csv
import pandas as pd

def prep_odiwc_data(input_folder, output_filename):
    print(f"🏆 Starting Men's ODI World Cup ETL Pipeline...")
    all_balls = []
    
    file_count = 0
    for filename in os.listdir(input_folder):
        if not filename.endswith(".csv"):
            continue
            
        file_count += 1
        filepath = os.path.join(input_folder, filename)
        match_id = filename.split('.')[0]
        
        match_info = {'match_id': match_id, 'teams': []}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row: continue
                    
                if row[0] == 'info':
                    key = row[1]
                    val = row[2]
                    if key == 'season': match_info['season'] = val
                    elif key == 'date': match_info['date'] = val
                    elif key == 'venue': match_info['venue'] = val
                    elif key == 'player_of_match': match_info['player_of_match'] = val
                    elif key == 'winner': match_info['match_won_by'] = val
                    elif key == 'team': match_info['teams'].append(val)
                
                elif row[0] == 'ball':
                    batting_team = row[3]
                    bowling_team = 'Unknown'
                    if len(match_info['teams']) >= 2:
                        bowling_team = match_info['teams'][1] if match_info['teams'][0] == batting_team else match_info['teams'][0]

                    ball_data = {
                        'match_id': match_id,
                        'date': match_info.get('date', 'Unknown'),
                        'venue': match_info.get('venue', 'Unknown'),
                        'match_won_by': match_info.get('match_won_by', 'Unknown'),
                        'player_of_match': match_info.get('player_of_match', 'Unknown'),
                        'batting_team': batting_team,
                        'bowling_team': bowling_team,
                        'innings': int(row[1]),
                        'ball': float(row[2]),
                        'batter': row[4],
                        'non_striker': row[5],
                        'bowler': row[6],
                        'runs_batter': int(row[7]),
                        'runs_extras': int(row[8]),
                    }
                    
                    if len(row) > 14 and row[14] != '':
                        ball_data['wicket_kind'] = row[14]
                        ball_data['player_out'] = row[15] if len(row) > 15 else ''
                    else:
                        ball_data['wicket_kind'] = None
                        ball_data['player_out'] = None
                        
                    all_balls.append(ball_data)

    df = pd.DataFrame(all_balls)
    df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
    df['year'] = df['date'].dt.year.fillna(0).astype(int).astype(str)
    df['year'] = df['year'].replace('0', 'Unknown')
    
    df.to_csv(output_filename, index=False)
    print(f"✅ ODI World Cup ETL Complete! Processed {file_count} matches.")
    print(f"📊 Total deliveries processed: {len(df):,}")

if __name__ == "__main__":
    INPUT_DIR = "data/ODIWC_Raw"
    OUTPUT_FILE = "data/odiwc_combined.csv"
    prep_odiwc_data(INPUT_DIR, OUTPUT_FILE)