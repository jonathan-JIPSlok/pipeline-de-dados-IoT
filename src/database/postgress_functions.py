from sqlalchemy import create_engine, Engine, text
from pathlib import Path
import pandas as pd
import logging

# Conexão com o banco de dados
def create_con(user, password, url, port, database) -> Engine:
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{url}:{port}/{database}')

# função para inserir dados no database
def insert_data(df: pd.DataFrame, name: str, engine: Engine):
    try:
        df.to_sql(
            name=name,
            con=engine
            )
    except Exception as error:
        logging.error("Funcao insert_data -> " + str(error))


# Função para carregar dados de uma view
def load_data(view_name: str, engine: Engine) -> pd.DataFrame:
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# Funçao para criar views
def CreateViewDatabase(engine: Engine, localSqlView: Path):
    try:
        with engine.connect() as conn:
            with open(localSqlView,'r') as file:
                sql = file.read()
            conn.execute(text(sql))
            conn.commit()
    except Exception as error:
        logging.error("Funcao create view database -> " + str(error))