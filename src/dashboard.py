from pathlib import Path
import os
from dotenv import load_dotenv
from database.postgress_functions import create_con, load_data
import plotly.express as px
import streamlit as st

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env a partir da pasta infra
env_path = BASE_DIR / "infra" / ".env"
if not load_dotenv(dotenv_path=env_path):
    raise Exception("Não foi possível importar os environments")

# Conectando com o database
engine = create_con(
    os.getenv("USER"),
    os.getenv("SECRET_KEY"),
    os.getenv("URL"),
    os.getenv("PORT"),
    os.getenv("DATABASE")
)
if __name__ == "__main__":
    st.title("Dashboard de Temperaturas IoT")

    # Gráfico com Máxima de In e Out por tempo e a diferença entre eles
    df = load_data("temp_in_out_diff", engine)
    df = df.sort_values("dia")
    fig1 = px.line(
        df,
        x="dia",
        y=["temperatura interna", "temperatura externa", "diferenca temperatura"],
        labels={"value": "Temperatura (ºC)", "dia": "Dia","variable": "Tipo temperatura"},
        title="Temperatura média diaria Interna, Externa e Diferença entre elas",
    )
    st.plotly_chart(fig1)

    # Gráfico médias interna e externa por dia
    df = load_data("vw_avg_month", engine)
    fig2 = px.bar(
        df,
        x="mes",
        y=["temperatura interna", "temperatura externa"],
        title="Média mensal temperatura interna e externa",
        barmode="group",
        labels={"value": "Temperatura (ºC)", "mes": "Mês","variable": "Tipo temperatura"}
    )
    fig2.update_layout(template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig2)

    # Gráfico de linha da diferença de temperatura
    df = load_data("diff_in_out_day", engine)
    fig3 = px.line(
        df.sort_values("dia"),
        x="dia",
        y="diferenca temperatura",
        labels={
            "dia": "Dia",
            "diferenca temperatura": "Diferença (Interna - Externa) ºC",
        },
        title="Diferença entre temperatura interna e externa por dia"
    )
    fig3.update_layout(template="plotly_white", hovermode="x unified")
    # Linha de referência no zero (quando interna = externa)
    fig3.add_hline(y=0, line_dash="dash", line_color="red")

    st.plotly_chart(fig3)

    