import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from Bio import SeqIO

st.sidebar.title('Secuencia Genética')
bcolor = st.sidebar.color_picker('Escoge un color :)', '#DBDEDB')
adn = st.sidebar.text_input('Ingrese la secuencia de ADN: ', "")





# Configuración de Streamlit
st.title("Selector de Gráficos")

# Selector para tipo de gráfico
graph_type = st.radio("Selecciona el tipo de gráfico:", ["Lineas", "Barras", "Barras Horizontales", "Histograma"])

# Función para generar gráficos
def generate_graph(option, graph_type):
    fig, ax = plt.subplots()  # Crear una figura
    x = np.linspace(0, 10, 100)  # Valores para el eje x
    y = None  # Inicialización de y para todas las opciones

    if graph_type == "Line":
        ax.plot(x, y, label=option)
    elif graph_type == "Bar":
        ax.bar(x[:10], y[:10], label=option)  # Graficar solo los primeros 10 valores
    elif graph_type == "Barh":
        ax.barh(x[:10], y[:10], label=option)  # Graficar solo los primeros 10 valores
    elif graph_type == "Hist":
        ax.hist(y, bins=20, label=option)

    ax.legend()
    ax.set_title(f"Gráfico de {option} ({graph_type})")
    ax.grid(True)
    return fig

# Mostrar el gráfico seleccionado
try:
    fig = generate_graph(adn, graph_type)  # Pasar 'adn' como 'option'
    st.pyplot(fig)  # Mostrar el gráfico en Streamlit
except Exception as e:
    st.error(f"¡Error al generar el gráfico: {e}!")



