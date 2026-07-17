import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.set_page_config(page_title="IA Caducidad Alimentos", page_icon="🍎")
st.title("🧠 Detector de Alimentos y Vida Útil")
st.write("Saca una foto o sube una imagen para calcular sus días estimados.")

@st.cache_resource
def cargar_modelo():
    return tf.keras.models.load_model('modelo_frutas_v1.keras')

modelo = cargar_modelo()
clases = ['apple', 'lettuce', 'pineapple', 'potato', 'strawberry', 'tomato']

tabla_caducidad = {'apple': 15, 'strawberry': 4, 'pineapple': 7, 'lettuce': 5, 'potato': 21, 'tomato': 6}
traducciones = {'apple': 'Manzana 🍎', 'strawberry': 'Fresa 🍓', 'pineapple': 'Piña 🍍', 'lettuce': 'Lechuga 🥬', 'potato': 'Papa 🥔', 'tomato': 'Tomate 🍅'}

archivo_imagen = st.file_uploader("Elige una foto...", type=["jpg", "jpeg", "png"])

if archivo_imagen is not None:
    imagen = Image.open(archivo_imagen)
    st.image(imagen, caption='Imagen subida', use_column_width=True)
    
    img_redimensionada = imagen.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img_redimensionada)
    img_array = np.expand_dims(img_array, axis=0)
    
    with st.spinner('Analizando alimento...'):
        predicciones = modelo.predict(img_array)
        indice = np.argmax(predicciones)
        alimento = clases[indice]
        certeza = float(predicciones[indice]) * 100
        
    st.success(f"### Alimento detectado: {traducciones.get(alimento, alimento.capitalize())}")
    st.metric(label="Certeza del análisis", value=f"{certeza:.2f}%")
    
    if alimento in tabla_caducidad:
        st.info(f"⏳ **Tiempo estimado de vida útil:** ¡Consumir en los próximos {tabla_caducidad[alimento]} días!")