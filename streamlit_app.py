import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO
import pandas as pd
import seaborn as sns

# Configuración de Streamlit
st.sidebar.title('Secuencia Genética')
seqadn = st.sidebar.text_input('Ingrese la secuencia de ADN: ', "")
bcolor = st.sidebar.color_picker('Escoge un color :)', '#DBDEDB')

def main():
with st.sidebar:
        api_options = ("echarts", "pyecharts")
        selected_api = st.selectbox(
            label="Choose your preferred API:",
            options=api_options,
        )

        if selected_api == "echarts":
            st.caption(
                """ECharts demos are extracted from https://echarts.apache.org/examples/en/index.html, 
            by copying/formattting the 'option' json object into st_echarts.
            Definitely check the echarts example page, convert the JSON specs to Python Dicts and you should get a nice viz."""
            )
        if selected_api == "pyecharts":
            st.caption(
                """Pyecharts demos are extracted from https://github.com/pyecharts/pyecharts-gallery,
            by copying the pyecharts object into st_pyecharts. 
            Pyecharts is still using ECharts 4 underneath, which is why the theming between st_echarts and st_pyecharts is different."""
            )

    demo()

    sourcelines, _ = inspect.getsourcelines(demo)

# Función para calcular la composición de nucleótidos
def nucleotides_composition(seqadn):
    nucleotides = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    if len(seqadn) == 0:  # Verificar que la secuencia no esté vacía
        return nucleotides  # Retornar 0% si la secuencia está vacía
    
    for n in nucleotides:
        nucleotides[n] = seqadn.count(n) / len(seqadn) * 100  # Calcula el porcentaje de cada nucleótido
    return nucleotides

# Calcular la composición de nucleótidos solo si la secuencia no está vacía
if seqadn != "":
    nuc = nucleotides_composition(seqadn)

    # Crear un DataFrame con los datos de la composición de nucleótidos
    ndf = pd.DataFrame.from_dict(nuc, orient='index')
    ndf = ndf.reset_index()
    ndf = ndf.rename(columns={"index": "Nucleotide", 0: "Composition"})

    # Selector para tipo de gráfico
    st.title("Selector de Gráficos")
    graph_type = st.radio("Selecciona el tipo de gráfico:", ["Gráfico de Pastel", "Barras", "Barras Horizontales", "Histograma"])

    # Función para generar gráficos
    def generate_graph(seqadn, graph_type, bcolor):
        fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura

        # Gráfico de pastel con la composición de nucleótidos
        if graph_type == "Gráfico de Pastel":
            # Los valores para el gráfico de pastel serán los porcentajes de composición de nucleótidos
            labels = list(nuc.keys())  # Nucleótidos: A, C, G, T
            sizes = list(nuc.values())  # Composición en porcentaje
            colors = [bcolor] * len(labels) # Usar el color seleccionado para todos los nucleótidos
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#F5CBED","#EFB3E3","#DA84C9","#BF63AD"])
            ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

        # Gráfico de barras con la composición de nucleótidos
        elif graph_type == "Barras":
            sns.set(style="whitegrid")
            sns.barplot(x="Nucleotide", y="Composition", data=ndf, ax=ax, color=bcolor)
            ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

        # Gráfico de barras horizontales
        elif graph_type == "Barras Horizontales":
            ax.barh(ndf["Nucleotide"], ndf["Composition"], color=bcolor)
            ax.set_title("Composición de Nucleótidos (Barras Horizontales)")

        # Histograma (esto no aplica directamente con ADN, pero lo dejo como ejemplo)
        elif graph_type == "Histograma":
            ax.hist(list(nuc.values()), bins=4, label="Composición", color=bcolor)
            ax.set_title("Histograma de Composición de Nucleótidos")

        # Ajustes del gráfico
        ax.legend()
        ax.set_xlabel("Nucleótidos")
        ax.set_ylabel("Composición (%)")
        ax.grid(True)

        return fig

    # Mostrar el gráfico seleccionado
    try:
        fig = generate_graph(seqadn, graph_type, bcolor)  # Pasar 'seqadn' como 'option'
        st.pyplot(fig)  # Mostrar el gráfico en Streamlit
    except Exception as e:
        st.error(f"¡Error al generar el gráfico: {e}!")
else:
    st.warning("Por favor ingrese una secuencia de ADN válida antes de comenzar.")


