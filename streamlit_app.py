import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

show_pages(
    [   
        Page("dezoomcamp/DE_Zoomcamp.py", "DE Zoomcamp", "💻"),
    ]
)

st.header("Biomoléculas")
st.image("https://www.shutterstock.com/image-illustration/molecules-3d-model-atoms-chemical-600nw-2499664001.jpg")

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
        composition = None

elif selected_api == "Proteína":
    if seq_input:  # Validar que se haya ingresado una secuencia
        composition = protein_composition(seq_input)
        title = "Bases de ARN"
    else:
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


st.sidebar.title("Resources")
st.sidebar.markdown(
    """
- [National Library of Medicine](https://www.ncbi.nlm.nih.gov)
"""
)

st.sidebar.title("Bibliografía")
st.sidebar.markdown(
    """
    - [Biomoléculas: carbohidratos, proteínas,
    lípidos y ácidos nucleicos.](https://www.unl.edu.ar/ingreso/cursos/medicina/wp-content/uploads/sites/8/2017/10/Quimica_09.pdf)
    - [Nucleótido.](https://www.genome.gov/es/genetics-glossary/Nucleotido)
    - [Proteína.](https://www.genome.gov/es/genetics-glossary/Proteina#)
 
"""
)

st.markdown("""

Las biomoléculas son las moléculas que forman parte de la estructura y funcionamiento de los organismos vivos. Estas incluyen macromoléculas como polisacáridos, lípidos, proteínas y ácidos nucleicos, así como sus unidades más pequeñas: monosacáridos, ácidos grasos, aminoácidos y nucleótidos. Aunque existen cientos de biomoléculas distintas, desde un enfoque práctico se agrupan en siete categorías principales, que también son esenciales en la dieta: carbohidratos, proteínas, lípidos, agua, minerales (iones), vitaminas y ácidos nucleicos. Los minerales, al disolverse en los líquidos del cuerpo, se convierten en iones, fundamentales para diversas funciones biológicas.
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
       
### Nucleótido

Un nucleótido es la unidad básica que compone los ácidos nucleicos, es decir, el ADN y el ARN, que son las moléculas responsables de almacenar y transmitir la información genética en los seres vivos. Cada nucleótido está formado por tres componentes principales: una molécula de azúcar, que puede ser ribosa (en el ARN) o desoxirribosa (en el ADN); un grupo fosfato, que actúa como un enlace entre nucleótidos para formar largas cadenas; y una base nitrogenada, que es la parte que varía y que determina las "letras" del código genético.
En el ADN, las bases nitrogenadas son adenina (A), guanina (G), citosina (C) y timina (T). En el ARN, la timina es reemplazada por el uracilo (U). Estos nucleótidos se enlazan uno tras otro para formar las largas cadenas que constituyen el ADN y el ARN, y las bases nitrogenadas interactúan entre sí (mediante enlaces específicos) para darle al ADN su característica estructura de doble hélice. Por lo tanto, los nucleótidos no solo son los "bloques de construcción" de los ácidos nucleicos, sino que también son esenciales para el almacenamiento y transmisión de la información genética.


#### Proteína

Las proteínas son moléculas grandes y complejas que desempeñan un papel esencial en casi todas las funciones del cuerpo humano. Actúan como los "trabajadores" principales de las células, ayudando en procesos tan variados como la construcción y mantenimiento de tejidos, el transporte de moléculas, la defensa contra infecciones y la regulación de actividades dentro del organismo.
Están formadas por cadenas largas de aminoácidos, que son como "bloques de construcción" conectados entre sí. Estas cadenas, llamadas polipéptidos, se pliegan de formas específicas para que la proteína pueda realizar su función. La secuencia de aminoácidos en una proteína está determinada por las instrucciones almacenadas en el ADN, lo que significa que cada proteína tiene una forma y función únicas según lo que el cuerpo necesita. Sin proteínas, el cuerpo no podría mantener su estructura ni llevar a cabo los procesos vitales que nos mantienen vivos y saludables.
""", unsafe_allow_html=True)

