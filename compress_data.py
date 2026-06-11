import os
import pandas as pd

data_dir = "data"
if os.path.exists(data_dir):
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            csv_path = os.path.join(data_dir, file)
            file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
            
            # If the file is larger than 50MB, convert it
            if file_size_mb > 50:
                print(f"Compressing {file} ({file_size_mb:.2f} MB)...")
                
                # Read the CSV and save as Parquet
                df = pd.read_csv(csv_path, low_memory=False)
                parquet_path = csv_path.replace(".csv", ".parquet")
                df.to_parquet(parquet_path, compression="snappy", index=False)
                
                # Delete the old heavy CSV file
                os.remove(csv_path)
                print(f"✅ Successfully converted to {os.path.basename(parquet_path)}")

print("Data compression optimization complete!")