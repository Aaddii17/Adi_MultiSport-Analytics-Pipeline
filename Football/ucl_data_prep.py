import pandas as pd
import os

def clean_encoding(text):
    """Repairs common UTF-8 to Windows-1252 corruption artifacts."""
    if pd.isna(text): return text
    text = str(text)
    text = text.replace('â‚¬"', '-')  # Fixes the 4â‚¬"3 scoreline issue
    text = text.replace('â€“', '-')
    text = text.replace('Ã©', 'é')    # Fixes AtlÃ©tico
    text = text.replace('Ã¼', 'ü')    # Fixes MÃ¼nchen
    return text.strip()

def prep_ucl_data(input_folder, output_folder):
    print("🏆 Initializing UEFA Champions League ETL Pipeline...")
    
    # 1. Clean the Finals History Table
    finals_path = os.path.join(input_folder, "ucl", "UCL_Finals_1955-2023.csv")
    if os.path.exists(finals_path):
        print("📥 Processing Finals History...")
        df_finals = pd.read_csv(finals_path, encoding='latin-1', on_bad_lines='skip')
        
        # Explicitly passing 'object' and 'string' silences the Pandas4Warning safely
        text_cols = df_finals.select_dtypes(include=['object', 'string']).columns
        for col in text_cols:
            df_finals[col] = df_finals[col].apply(clean_encoding)
            
        df_finals.to_csv(os.path.join(output_folder, "ucl_finals_clean.csv"), index=False)
        print("✅ Finals History Cleaned!")

    # 2. Clean the All-Time Performance Table
    alltime_path = os.path.join(input_folder, "ucl", "UCL_AllTime_Performance_Table.csv")
    if os.path.exists(alltime_path):
        print("📥 Processing All-Time Leaderboard...")
        df_alltime = pd.read_csv(alltime_path, encoding='latin-1', on_bad_lines='skip')
        
        if 'Team' in df_alltime.columns:
            df_alltime['Team'] = df_alltime['Team'].apply(clean_encoding)
            
        if 'goals' in df_alltime.columns:
            df_alltime.drop(columns=['goals'], inplace=True)
            
        df_alltime.to_csv(os.path.join(output_folder, "ucl_alltime_clean.csv"), index=False)
        print("✅ All-Time Leaderboard Cleaned!")

    # 3. Extract the Goal Event Data from the Excel Workbook
    excel_path = os.path.join(input_folder, "ucl", "UEFA Champions League 2016-2022 Data.xlsx")
    if os.path.exists(excel_path):
        print("📥 Processing Goal Events Data (This may take a moment)...")
        try:
            # openpyxl engine will now pick this up seamlessly
            df_goals = pd.read_excel(excel_path, sheet_name='goals')
            df_goals.to_csv(os.path.join(output_folder, "ucl_goals_clean.csv"), index=False)
            print("✅ Goal Events Extracted!")
        except Exception as e:
            print(f"⚠️ Could not load Excel file: {e}")

    print("🏆 UCL ETL Pipeline Complete!")

if __name__ == "__main__":
    DATA_DIR = "../data/" if os.path.exists("../data/") else "data/"
    prep_ucl_data(DATA_DIR, DATA_DIR)