import pandas as pd
import os

def clean_encoding(text):
    """Repairs common UTF-8 to Windows-1252 corruption artifacts in scraped football data."""
    if pd.isna(text): return text
    text = str(text)
    text = text.replace('â‚¬"', '-')
    text = text.replace('â€“', '-')
    text = text.replace('Ã©', 'é')    # Mbappé
    text = text.replace('Ã¼', 'ü')    # Müller
    text = text.replace('Ã¡', 'á')    # Stábile
    text = text.replace('Ã³', 'ó')    # Ronaldo
    text = text.replace('Ã±', 'ñ')    # España
    text = text.replace('Ã', 'í')     # Catch-all for residual i-accents
    return text.strip()

def prep_fifa_data(input_folder, output_folder):
    print("🌍 Initializing FIFA World Cup ETL Pipeline...")
    
    # 1. Process World Cup Tournament Summary
    wc_path = os.path.join(input_folder, "fifa", "world_cup.csv")
    if os.path.exists(wc_path):
        print("📥 Processing Tournament History...")
        df_wc = pd.read_csv(wc_path, encoding='latin-1', on_bad_lines='skip')
        
        # Clean string columns
        text_cols = df_wc.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_wc[col] = df_wc[col].apply(clean_encoding)
            
        # SPLIT TOP SCORER: "Kylian Mbappé - 8" -> "Kylian Mbappé" and "8"
        if 'TopScorrer' in df_wc.columns:
            # rsplit by '-' only on the last occurrence in case a player has a hyphenated name
            split_data = df_wc['TopScorrer'].str.rsplit('-', n=1, expand=True)
            df_wc['Top Scorer Name'] = split_data[0].str.strip()
            df_wc['Top Scorer Goals'] = pd.to_numeric(split_data[1], errors='coerce').fillna(0).astype(int)
            df_wc.drop(columns=['TopScorrer'], inplace=True)
            
        df_wc.to_csv(os.path.join(output_folder, "fifa_worldcup_clean.csv"), index=False)
        print("✅ Tournament Summary Cleaned!")

    # 2. Process Granular Match Data
    matches_path = os.path.join(input_folder, "fifa", "matches_1930_2022.csv")
    if os.path.exists(matches_path):
        print("📥 Processing Match Data (1930-2022)...")
        df_matches = pd.read_csv(matches_path, encoding='latin-1', on_bad_lines='skip')
        
        text_cols = df_matches.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_matches[col] = df_matches[col].apply(clean_encoding)
            
        # Standardize score columns so we can build the all-time table
        df_matches['home_score'] = pd.to_numeric(df_matches['home_score'], errors='coerce').fillna(0).astype(int)
        df_matches['away_score'] = pd.to_numeric(df_matches['away_score'], errors='coerce').fillna(0).astype(int)
        
        # Calculate Match Result (W, D, L) for points table logic
        import numpy as np
        conditions = [
            (df_matches['home_score'] > df_matches['away_score']),
            (df_matches['home_score'] < df_matches['away_score'])
        ]
        df_matches['ftr'] = np.select(conditions, ['H', 'A'], default='D')
        
        df_matches.to_csv(os.path.join(output_folder, "fifa_matches_clean.csv"), index=False)
        print("✅ Match Data Cleaned!")

    print("🏆 FIFA ETL Pipeline Complete!")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    prep_fifa_data(DATA_DIR, DATA_DIR)