
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd


@dataclass
class SubFlow:
    source_step: str
    source_files: list[str]
    target_step: str
    target_file: str

@dataclass
class ETLProject:
    name: str
    steps: Dict[str, list[str]]                 # step -> list of files(full paths)
    dataframes: Dict[str, pd.DataFrame]         # step -> consolidated dataframe
    subflows: List[SubFlow]                     # relationships between files in steps