import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

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

st.title('Show Proteins')
