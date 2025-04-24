import os

def read_files_from_step(step_name: str, folder_path: str):
    files = [f for f in os.listdir(folder_path) if f.endswith(('.csv', '.parquet'))]
    dataframes = []

    for file in files:
        full_path = os.path.join(folder_path, file)
        