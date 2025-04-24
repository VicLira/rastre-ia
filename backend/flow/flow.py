import os
from typing import Dict, List

import pandas as pd
from flow.project import ETLProject, SubFlow
from flow.interface_reader import DataReader
from utils.logger import logger


class DataFlow:
    def __init__(self, reader: DataReader):
        self.steps: Dict[str, pd.DataFrame] = {}
        self.reader = reader

    def add_step(self, step_name: str, folder_path: str) -> None:
        if step_name in self.steps:
            logger.warning(f"Step '{step_name}' alredy exists. Replacing.")
        df = self.reader.read_folder(folder_path)
        self.steps[step_name] = df
        logger.info(f"Step '{step_name}' added: {df.shape[0]} linhas, {df.shape[1]} colunas.")

    def show_summary(self) -> None:
        print("\nResumo do fluxo:")
        for name, df in self.steps.items():
            print(f"- {name}: {df.shape[0]} linhas | {df.shape[1]} colunas")

    def get_steps(self) -> Dict[str, pd.DataFrame]:
        return self.steps
    
    def list_files(arquivos: List[str]) -> None:
        for idx, f in enumerate(arquivos):
            print(f"[{idx}] {os.path.basename(f)}")


    def create_subflow(source_step: str, source_files: List[str], target_step: str, target_file: str) -> SubFlow:
        return SubFlow(
            source_step=source_step,
            source_files=source_files,
            target_step=target_step,
            target_file=target_file
        )