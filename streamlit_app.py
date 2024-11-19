import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# Función para obtener información de proteínas

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
bcolor = st.sidebar.color_picker('Pick A Color', '#DBDEDB')
protein = st.sidebar.text_input('Ingrese la secuencia de ADN: ', "")

if protein != "":
    # Obtener información de la proteína
    descriptor, title = get_protein_info(protein)

    if descriptor and title:
        st.sidebar.markdown(f'**{descriptor}**')
        st.sidebar.markdown(f'**{title}**')

        # Visualización 3D de la proteína usando py3Dmol
        xyzview = py3Dmol.view(query=f'pdb:{protein}')
        xyzview.setStyle({'stick': {}})  # Define el estilo de la visualización (por ejemplo, estilo 'stick')
        xyzview.setBackgroundColor("white")  # Configura el color de fondo

        # Condición para hacer girar la molécula
        spin = st.sidebar.checkbox("Girar molécula")
        if spin:
            xyzview.spin(True)
        else:
            xyzview.spin(False)

        # Ajusta el zoom de la visualización
        xyzview.zoomTo()

        # Mostrar la visualización en la aplicación de Streamlit
        st.py3Dmol(xyzview, height=500, width=800)
    else:
        st.sidebar.error("No se pudo obtener información de la proteína.")

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
    fig = generate_graph(protein, graph_type)  # Pasar 'protein' como 'option'
    st.pyplot(fig)  # Mostrar el gráfico en Streamlit
except Exception as e:
    st.error(f"¡Error al generar el gráfico: {e}!")



