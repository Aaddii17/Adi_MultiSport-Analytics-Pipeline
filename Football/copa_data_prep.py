import pandas as pd
import os

def clean_encoding_and_typos(text):
    """Repairs encodings and specific data entry typos."""
    if pd.isna(text): return text
    text = str(text)
    text = text.replace('Cheli', 'Chile')  # Fixes the massive typo in the raw data
    text = text.replace('Ã§Ã£', 'çã')
    return text.strip()

def prep_copa_data(input_folder, output_folder):
    print("🌎 Initializing Copa America ETL Pipeline...")
    
    # 1. Process Tournament Summary
    summary_path = os.path.join(input_folder, "copa", "copa_america.csv")
    if os.path.exists(summary_path):
        print("📥 Processing Tournament History...")
        df_summary = pd.read_csv(summary_path, encoding='latin-1', on_bad_lines='skip')
        
        # Clean up column names
        rename_map = {
            'Runners U': 'Runner-Up',
            'Total Tean': 'Teams',
            'Total Matc': 'Matches',
            'Average g': 'Average Goals',
            'Total Goal': 'Total Goals'
        }
        df_summary.rename(columns=rename_map, inplace=True)
        
        # Apply typo fixes to text columns
        text_cols = df_summary.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_summary[col] = df_summary[col].apply(clean_encoding_and_typos)
            
        df_summary.to_csv(os.path.join(output_folder, "copa_summary_clean.csv"), index=False)
        print("✅ Tournament Summary Cleaned and Translated!")

    # 2. Process Match Data (Translating Portuguese to English)
    matches_path = os.path.join(input_folder, "copa", "Copa_America 2001-2021.csv")
    if os.path.exists(matches_path):
        print("📥 Processing Match Data (2001-2021)...")
        df_matches = pd.read_csv(matches_path, encoding='latin-1', on_bad_lines='skip')
        
        # Portuguese to English Translation Map
        pt_to_en = {
            'Data': 'Date',
            'Casa': 'Home Team',
            'Fora': 'Away Team',
            'Gols Casa': 'Home Score',
            'Gols Fora': 'Away Score',
            'Fase': 'Round'
        }
        
        # Dynamically catch the corrupted 'EdiÃ§Ã£o' column for Year
        for col in df_matches.columns:
            if 'Edi' in col:
                pt_to_en[col] = 'Year'
                
        df_matches.rename(columns=pt_to_en, inplace=True)
        
        text_cols = df_matches.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_matches[col] = df_matches[col].apply(clean_encoding_and_typos)
            
        df_matches.to_csv(os.path.join(output_folder, "copa_matches_clean.csv"), index=False)
        print("✅ Match Data Translated and Cleaned!")

    print("🏆 Copa America ETL Pipeline Complete!")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    prep_copa_data(DATA_DIR, DATA_DIR)