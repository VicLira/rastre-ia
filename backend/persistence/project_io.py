import json
import os
from utils.logger import logger
from flow.project import ETLProject, SubFlow
import pandas as pd

def save_project(project: ETLProject, directory: str = "projects"):
    os.makedirs(directory, exist_ok=True)

    json_path = os.path.join(directory, f"{project.name}.json")

    project_dict = {
        "name": project.name,
        "steps": project.steps,
        "subflows": [
            {
                "source_step": s.source_step,
                "__source_file": s.source_files,
                "target_step": s.target_step,
                "target_file": s.target_file
            }
            for s in project.subflows
        ]
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(project_dict, f, indent=2)

    logger.info(f"✅ Projeto '{project.name}' salvo em {json_path}")

def load_project(name: str, directory: str = "projects") -> ETLProject:
    path = os.path.join(directory, f"{name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Projeto '{name}' não encontrado em {directory}")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Carregar os DataFrames
    dataframes = {}
    for step, files in data["steps"].items():
        dfs = []
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(file, sep=";", encoding="latin-1")
            elif file.endswith(".parquet"):
                df = pd.read_parquet(file)
            else:
                continue
            df["__source_file"] = os.path.basename(file)
            dfs.append(df)
            
        dataframes[step] = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        
    subflows = [SubFlow(**s) for s in data["subflows"]]
    
    return ETLProject(
        name=data["name"],
        steps=data["steps"],
        dataframes=dataframes,
        subflows=subflows
    )