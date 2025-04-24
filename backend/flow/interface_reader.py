import pandas as pd


class DataReader:
    def read_folder(self, path: str) -> pd.DataFrame:
        raise NotImplementedError("Subclasses devem implementar este método.")