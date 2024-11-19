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

# Función para calcular la composición de nucleótidos
def nucleotides_composition(seqadn):
    nucleotides = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for n in nucleotides:
        nucleotides[n] = seqadn.count(n) / len(seqadn) * 100  # Calcula el porcentaje de cada nucleótido
    return nucleotides

# Calcular la composición de nucleótidos
nuc = nucleotides_composition(seqadn)

# Crear un DataFrame con los datos de la composición de nucleótidos
ndf = pd.DataFrame.from_dict(nuc, orient='index')
ndf = ndf.reset_index()
ndf = ndf.rename(columns={"index": "Nucleotide", 0: "Composition"})

# Selector para tipo de gráfico
st.title("Selector de Gráficos")
graph_type = st.radio("Selecciona el tipo de gráfico:", ["Lineas", "Barras", "Barras Horizontales", "Histograma"])

# Función para generar gráficos
def generate_graph(seqadn, graph_type):
    fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura

    # Gráfico de líneas (sin usar, porque no tiene sentido con ADN directamente)
    x = np.linspace(0, 10, 100)  # Valores para el eje x
    y = np.sin(x)  # Ejemplo para un gráfico de líneas, si se decide usar
    if graph_type == "Lineas":
        ax.plot(x, y, label="Ejemplo de línea")
        
    # Gráfico de barras con la composición de nucleótidos
    elif graph_type == "Barras":
        sns.set(style="whitegrid")
        sns.barplot(x="Nucleotide", y="Composition", data=ndf, ax=ax)
        ax.set_title("Composición de Nucleótidos en la Secuencia de ADN")

    # Gráfico de barras horizontales
    elif graph_type == "Barras Horizontales":
        ax.barh(ndf["Nucleotide"], ndf["Composition"])
        ax.set_title("Composición de Nucleótidos (Barras Horizontales)")

    # Histograma (esto no aplica directamente con ADN, pero lo dejo como ejemplo)
    elif graph_type == "Histograma":
        ax.hist(list(nuc.values()), bins=4, label="Composición")
        ax.set_title("Histograma de Composición de Nucleótidos")

    # Ajustes del gráfico
    ax.legend()
    ax.set_xlabel("Nucleótidos")
    ax.set_ylabel("Composición (%)")
    ax.grid(True)
    
    return fig

# Mostrar el gráfico seleccionado
try:
    if seqadn != "":
        fig = generate_graph(seqadn, graph_type)  # Pasar 'seqadn' como 'option'
        st.pyplot(fig)  # Mostrar el gráfico en Streamlit
    else:
        st.warning("Por favor ingrese una secuencia de ADN.")
except Exception as e:
    st.error(f"¡Error al generar el gráfico: {e}!")
   
