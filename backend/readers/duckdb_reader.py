import os
import duckdb
import pandas as pd

from flow.interface_reader import DataReader
from utils.logger import logger


class DuckDBReader(DataReader):
    def read_folder(self, path: str) -> pd.DataFrame:
        files = [f for f in os.listdir(path) if f.endswith(('.csv', '.parquet'))]
        dataframes = []

        for file in files:
            full_path = os.path.join(path, file)
            logger.info(f"Reading file: {full_path}")

            try:
                if file.endswith('.csv'):
                    query = f"""
                        SELECT * FROM read_csv_auto('{full_path}',
                            header=True,
                            ignore_errors=True
                        )
                    """
                    df = duckdb.query(query).to_df()
                    
                elif file.endswith('.parquet'):
                    df = duckdb.query(f"SELECT * FROM '{full_path}'").to_df()
                else:
                    continue

                df['__origem_file'] = file
                dataframes.append(df)

            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
        
        if dataframes:
            return pd.concat(dataframes, ignore_index=True)
        else:
            logger.warning(f"No CSV or parquet files found at {path}")
            return pd.DataFrame()
            