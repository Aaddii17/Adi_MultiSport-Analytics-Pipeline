import pandas as pd
import glob

print("🔍 Scanning Data Files...")
for file in glob.glob("data/epl_raw*.csv"):
    try:
        # Read just the very first row to get the column headers
        df = pd.read_csv(file, nrows=0)
        print(f"\n📄 File: {file}")
        print(f"Columns: {df.columns.tolist()[:15]}") 
    except Exception as e:
        print(f"\n⚠️ Error reading {file}: {e}")
        print("💡 Hint: If this was an Excel file, make sure you opened it and used 'Save As > CSV'.")