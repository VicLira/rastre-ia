from persistence.project_io import load_project, save_project
from utils.logger import logger
from flow.flow import DataFlow
from readers.duckdb_reader import DuckDBReader
from flow.project import ETLProject, SubFlow  # novo nome para 'projeto.py'
import os

def create_etl_project() -> ETLProject:
    project_name = input("Nome do projeto ETL: ").strip()
    reader = DuckDBReader()
    flow = DataFlow(reader)

    step_file_map = {}     # etapa -> lista de arquivos usados
    dataframes = {}        # etapa -> dataframe consolidado

    while True:
        step_name = input("Nome da etapa (ex: raw, cleaned, enriched): ").strip()
        folder_path = input("Caminho da pasta com arquivos da etapa: ").strip()

        # Detectar arquivos
        files = [os.path.join(folder_path, f)
                 for f in os.listdir(folder_path)
                 if f.endswith(('.csv', '.parquet'))]

        step_file_map[step_name] = files

        flow.add_step(step_name, folder_path)
        dataframes[step_name] = flow.get_steps()[step_name]

        continuar = input("Deseja adicionar outra etapa? (s/n): ").strip().lower()
        if continuar != 's':
            break

    # Projeto montado com base no que foi lido
    project = ETLProject(
        name=project_name,
        steps=step_file_map,
        dataframes=dataframes,
        subflows=[]  # será preenchido na Etapa 2
    )

    logger.info(f"\n✅ Projeto '{project_name}' criado com {len(step_file_map)} etapas:")
    for etapa, arquivos in step_file_map.items():
        logger.info(f"- {etapa}: {len(arquivos)} arquivos")

    return project

def map_subflows(projeto: ETLProject):
    while True:
        if input("\nDeseja mapear um subfluxo? (s/n): ").strip().lower() != 's':
            break

        src_step = input("Etapa de origem: ").strip()
        DataFlow.list_files(projeto.steps[src_step])
        src_idxs = [int(i) for i in input("Índices dos arquivos origem: ").split(',')]
        src_files = [projeto.steps[src_step][i] for i in src_idxs]

        tgt_step = input("Etapa de destino: ").strip()
        DataFlow.list_files(projeto.steps[tgt_step])
        tgt_idx = int(input("Índice do arquivo destino: "))
        tgt_file = projeto.steps[tgt_step][tgt_idx]

        sub = DataFlow.create_subflow(src_step, src_files, tgt_step, tgt_file)
        projeto.subflows.append(sub)
        logger.info(f"✅ Subfluxo: {src_step} → {tgt_step}/{os.path.basename(tgt_file)}")


def select_or_create_project() -> ETLProject:
    os.makedirs("projects", exist_ok=True)
    existing_projects = [f[:-5] for f in os.listdir("projects") if f.endswith(".json")]

    if existing_projects:
        logger.info("Projetos existentes:")
        for i, name in enumerate(existing_projects):
            logger.info(f"[{i}] {name}")
            
        choice = input("Deseja (n)ovo projeto ou carregar existente (indice)? ").strip().lower()
        if choice != 'n' and choice.isdigit()   :
            return load_project(existing_projects[int(choice)])
        
    return create_etl_project()  


if __name__ == "__main__":
    project = select_or_create_project()
    map_subflows(project)
    save_project(project)
