import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.header("Biomoléculas")

# Configuración de Streamlit
st.sidebar.title('Configuración')

# Función para calcular la composición de nucleótidos
def nucleotides_composition(seqadn):
    nucleotides = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    if len(seqadn) == 0:  # Verificar que la secuencia no esté vacía
        return nucleotides  # Retornar 0% si la secuencia está vacía
    
    for n in nucleotides:
        nucleotides[n] = seqadn.upper().count(n) / len(seqadn) * 100  # Calcula el porcentaje de cada nucleótido
    return nucleotides

# Función para calcular la composición de bases en ARN
def protein_composition(seqarn):
    proteina = {'A': 0, 'C': 0, 'G': 0, 'U': 0}
    if len(seqarn) == 0:  # Verificar que la secuencia no esté vacía
        return proteina  # Retornar 0% si la secuencia está vacía
    
    for p in proteina:
        proteina[p] = seqarn.upper().count(p) / len(seqarn) * 100  # Calcula el porcentaje de cada base
    return proteina

# Sidebar para seleccionar opciones
with st.sidebar:
    api_options = ("Nucleótido", "Proteína")
    selected_api = st.selectbox(
        label="Escoge el tipo de biomolécula:",
        options=api_options,
    )
    seq_input = st.text_input('Ingrese la secuencia: ', "")
    bcolor = st.color_picker('Escoge un color :)', '#DBDEDB')

# Lógica para Nucleótidos y Proteínas
if selected_api == "Nucleótido":
    if seq_input:  # Validar que se haya ingresado una secuencia
        composition = nucleotides_composition(seq_input)
        title = "Nucleótidos"
    else:
        st.warning("Por favor, ingrese una secuencia de ADN válida antes de comenzar.")
        composition = None

elif selected_api == "Proteína":
    if seq_input:  # Validar que se haya ingresado una secuencia
        composition = protein_composition(seq_input)
        title = "Bases de ARN"
    else:
        st.warning("Por favor, ingrese una secuencia de ARN válida antes de comenzar.")
        composition = None

# Crear gráficos si la composición es válida
if composition:
    # Crear un DataFrame con los datos de la composición
    df = pd.DataFrame.from_dict(composition, orient='index').reset_index()
    df = df.rename(columns={"index": title, 0: "Composition"})

    # Selector para tipo de gráfico
    st.title(f"Composición de {title}")
    graph_type = st.radio(
        "Selecciona el tipo de gráfico:", 
        ["Gráfico de Pastel", "Gráfico de Barras", "Gráfico de Barras Horizontales", "Gráfico de Área"]
    )

    # Función para generar gráficos
    def generate_graph(graph_type, bcolor):
        fig, ax = plt.subplots(figsize=(8, 6))  # Crear una figura

        if graph_type == "Gráfico de Pastel":
            labels = list(composition.keys())
            sizes = list(composition.values())
            st.subheader("Selecciona colores para cada nucleótido:")
            colors = []
            
            for label in labels:
                color = st.color_picker(f"Color para {label}", "#FFFFFF")
                colors.append(color)
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
                   colors=colors)
            ax.set_title(f"Composición de {title}")

        elif graph_type == "Gráfico de Barras":
            sns.set(style="whitegrid")
            sns.barplot(x=title, y="Composition", data=df, ax=ax, color=bcolor)
            ax.set_title(f"Composición de {title}")

        elif graph_type == "Gráfico de Barras Horizontales":
            ax.barh(df[title], df["Composition"], color=bcolor)
            ax.set_title(f"Composición de {title} (Barras Horizontales)")

        elif graph_type == "Gráfico de Área":
            x = df[title]
            y = df["Composition"]
            ax.fill_between(x, y, color=bcolor, alpha=0.7)
            ax.plot(x, y, color="black", marker="o")  # Línea y puntos en el gráfico
            ax.set_title(f"Gráfico de Área de Composición de {title}")

        ax.set_xlabel(title)
        ax.set_ylabel("Composición (%)")
        ax.grid(True)

        return fig

    try:
        fig = generate_graph(graph_type, bcolor)
        st.pyplot(fig)  # Mostrar el gráfico en Streamlit
    except Exception as e:
        st.error(f"¡Error al generar el gráfico: {e}!")

st.sidebar.header(_("Resources"))
st.sidebar.markdown(_(
    """
- [National Library of Medicine](https://www.ncbi.nlm.nih.gov)
