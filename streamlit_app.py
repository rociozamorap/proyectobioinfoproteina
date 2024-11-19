import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

from Bio.PDB import PDBParser, PDBList
from Bio.SeqUtils import seq1
from Bio.PDB.Polypeptide import CaPPBuilder
from Bio.PDB.Atom import Atom
from biopandas.pdb import PandasPdb
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import py3Dmol

# Función para obtener información de proteínas
def get_protein_info(prot):
    try:
        req = requests.get(f'https://data.rcsb.org/rest/v1/core/entry/{prot}/')
        prot_data = json.loads(req.text)
        title = prot_data["struct"]["title"]
        descriptor = prot_data["struct"]["pdbx_descriptor"]
        return descriptor, title
    except Exception as e:
        return None, f"Error al obtener información de la proteína: {e}"

# Configuración de Streamlit
st.sidebar.title('Proteina')
protein = st.sidebar.text_input('Ingrese la secuencia de ADN:', "")

st.title("Selector de Gráficos")

options = ["Seno", "Coseno", "Tangente", "Logaritmo"]
selection = st.radio("Selecciona un gráfico:", options)

# Función para generar gráficos
def generate_graph(option):
    fig, ax = plt.subplots()  # Crear una figura
    x = np.linspace(0, 10, 100)  # Valores para el eje x

    if option == "Seno":
        ax.plot(x, np.sin(x), label="Seno", color="blue")
    elif option == "Coseno":
        ax.plot(x, np.cos(x), label="Coseno", color="green")
    elif option == "Tangente":
        ax.plot(x, np.tan(x), label="Tangente", color="red")
    elif option == "Logaritmo":
        ax.plot(x, np.log(x + 1), label="Logaritmo", color="purple")

    ax.legend()
    ax.set_title(f"Gráfico de {option}")
    ax.grid(True)
    return fig

# Mostrar el gráfico seleccionado
try:
    fig = generate_graph(selection)
    st.pyplot(fig)  # Mostrar el gráfico en Streamlit
except Exception as e:
    st.error(f"¡Error al generar el gráfico: {e}!")

