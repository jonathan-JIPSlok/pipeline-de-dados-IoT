from script_reader.csv_reader import reader
from database.postgress_functions import insert_data, create_con, CreateViewDatabase, load_data
from dotenv import load_dotenv
import os
from pathlib import Path
import pandas as pd

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env a partir da pasta infra
env_path = BASE_DIR / "infra" / ".env"
if not load_dotenv(dotenv_path=env_path):
    raise Exception("Não foi possível importar os environments")

#Caminho para arquivo de dados
FILE_PATH = BASE_DIR / "data" / "IOT-temp.csv"

if __name__ == "__main__":

    # Conectando com o database
    engine = create_con(
        os.getenv("USER"),
        os.getenv("SECRET_KEY"),
        os.getenv("URL"),
        os.getenv("PORT"),
        os.getenv("DATABASE")
    )

    df = reader(FILE_PATH)

    # Convertendo a coluda noted_date para o formato "%y-%m-%d"
    df["noted_date"] = pd.to_datetime(df["noted_date"], format='mixed')

    # Inserindo dados
    insert_data(df,"temperature_readings", engine)

    # Criando as views
    view = BASE_DIR / "src" / "views" / "temp_in_out_diff.sql"
    CreateViewDatabase(
        engine=engine,
        localSqlView=view
    )
    
    view = BASE_DIR / "src" / "views" / "vw_avg_month.sql"
    CreateViewDatabase(
        engine=engine,
        localSqlView=view
    )

    view = BASE_DIR / "src" / "views" / "diff_in_out_day.sql"
    CreateViewDatabase(
        engine=engine,
        localSqlView=view
    )