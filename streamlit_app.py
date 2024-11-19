import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO
import pandas as pd
import seaborn as sns

# Configuración de Streamlit
st.sidebar.title('Secuencia Genética')

# Función para calcular la composición de nucleótidos
def nucleotides_composition(seqadn):
    nucleotides = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    if len(seqadn) == 0:  # Verificar que la secuencia no esté vacía
        return nucleotides  # Retornar 0% si la secuencia está vacía
    
    for n in nucleotides:
        nucleotides[n] = seqadn.upper().count(n) / len(seqadn) * 100  # Calcula el porcentaje de cada nucleótido
    return nucleotides

def protein_composition(seqadn):
    proteina = {'A': 0, 'C': 0, 'G': 0, 'U': 0}
    if len(seqadn) == 0:  # Verificar que la secuencia no esté vacía
        return nucleotides  # Retornar 0% si la secuencia está vacía
    
    for p in proteina:
        proteina[p] = seqadn.upper().count(n) / len(seqadn) * 100  # Calcula el porcentaje de cada proteina
    return proteina

with st.sidebar:
    api_options = ("Nucleótido", "Proteína")
    selected_api = st.selectbox(
        label="Escoge el tipo de biomolécula:",
        options=api_options,
    )
    seqadn = st.text_input('Ingrese la secuencia de ADN: ', "")
    bcolor = st.color_picker('Escoge un color :)', '#DBDEDB')

if selected_api == "Nucleótido":
    if seqadn:  # Validar que se haya ingresado una secuencia
        nuc = nucleotides_composition(seqadn)

        # Crear un DataFrame con los datos de la composición de nucleótidos
        ndf = pd.DataFrame.from_dict(nuc, orient='index').reset_index()
        ndf = ndf.rename(columns={"index": "Nucleotide", 0: "Composition"})

        # Selector para tipo de gráfico
        st.title("Selector de Gráficos")
        graph_type = st.radio(
            "Selecciona el tipo de gráfico:", 
            ["Gráfico de Pastel", "Barras", "Barras Horizontales", "Histograma"]
        )

        # Función para generar gráficos
        def generate_graph(graph_type, bcolor):
            fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura

            if graph_type == "Gráfico de Pastel":
                labels = list(nuc.keys())
                sizes = list(nuc.values())
                # Selector de colores dinámicos
    st.subheader("Selecciona colores para cada nucleótido:")
    colors = []
    for label in labels:
        color = st.color_picker(f"Color para {label}", "#FFFFFF")
        colors.append(color)
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
                       colors=colors)
                ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

            elif graph_type == "Barras":
                sns.set(style="whitegrid")
                sns.barplot(x="Nucleotide", y="Composition", data=ndf, ax=ax, color=bcolor)
                ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

            elif graph_type == "Barras Horizontales":
                ax.barh(ndf["Nucleotide"], ndf["Composition"], color=bcolor)
                ax.set_title("Composición de Nucleótidos (Barras Horizontales)")

            elif graph_type == "Histograma":
                ax.hist(list(nuc.values()), bins=4, label="Composición", color=bcolor)
                ax.set_title("Histograma de Composición de Nucleótidos")

            ax.set_xlabel("Nucleótidos")
            ax.set_ylabel("Composición (%)")
            ax.grid(True)

            return fig

        try:
            fig = generate_graph(graph_type, bcolor)
            st.pyplot(fig)  # Mostrar el gráfico en Streamlit
        except Exception as e:
            st.error(f"¡Error al generar el gráfico: {e}!")
    else:
        st.warning("Por favor, ingrese una secuencia de ADN válida antes de comenzar.")

elif selected_api == "Proteína":
if seqadn:  # Validar que se haya ingresado una secuencia
        prot = protein_composition(seqadn)

        # Crear un DataFrame con los datos de la composición de nucleótidos
        ndf = pd.DataFrame.from_dict(nuc, orient='index').reset_index()
        ndf = ndf.rename(columns={"index": "Nucleotide", 0: "Composition"})

        # Selector para tipo de gráfico
        st.title("Selector de Gráficos")
        graph_type = st.radio(
            "Selecciona el tipo de gráfico:", 
            ["Gráfico de Pastel", "Barras", "Barras Horizontales", "Histograma"]
        )

        # Función para generar gráficos
        def generate_graph(graph_type, bcolor):
            fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura

            if graph_type == "Gráfico de Pastel":
                labels = list(nuc.keys())
                sizes = list(nuc.values())
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
                       colors=["#F5CBED", "#EFB3E3", "#DA84C9", "#BF63AD"])
                ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

            elif graph_type == "Barras":
                sns.set(style="whitegrid")
                sns.barplot(x="Nucleotide", y="Composition", data=ndf, ax=ax, color=bcolor)
                ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

            elif graph_type == "Barras Horizontales":
                ax.barh(ndf["Nucleotide"], ndf["Composition"], color=bcolor)
                ax.set_title("Composición de Nucleótidos (Barras Horizontales)")

            elif graph_type == "Histograma":
                ax.hist(list(nuc.values()), bins=4, label="Composición", color=bcolor)
                ax.set_title("Histograma de Composición de Nucleótidos")

            ax.set_xlabel("Nucleótidos")
            ax.set_ylabel("Composición (%)")
            ax.grid(True)

            return fig

        try:
            fig = generate_graph(graph_type, bcolor)
            st.pyplot(fig)  # Mostrar el gráfico en Streamlit
        except Exception as e:
            st.error(f"¡Error al generar el gráfico: {e}!")
    else:
        st.warning("Por favor, ingrese una secuencia de ADN válida antes de comenzar.")
