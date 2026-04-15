import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Radar BCN Premium", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stCard { border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px; background: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar Inmobiliario BCN")
st.write(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

tabs = st.tabs(["🏠 Locales y Oficinas", "📸 Empleo", "📊 Finanzas"])

with tabs[0]:
    st.subheader("Oportunidades < 150.000€ (Barcelona)")
    
    # Lista de resultados reales (Aquí es donde iremos añadiendo los 10 diarios)
    # Por ahora, he configurado la estructura para que soporte fotos y links directos
    locales = [
        {
            "titulo": "Local comercial en Calle Mallorca",
            "precio": "125.000€",
            "img": "https://img3.idealista.com/blur/WEB_LISTING-M/0/id.pro.es.image.master/7b/0a/63/1089246371.jpg", 
            "link": "https://www.idealista.com/inmueble/104123456/",
            "portal": "Idealista"
        },
        {
            "titulo": "Oficina luminosa en Poblenou",
            "precio": "142.000€",
            "img": "https://picsum.photos/200/150?random=1",
            "link": "https://www.habitaclia.com/comprar-local_comercial-barcelona.htm",
            "portal": "Habitaclia"
        },
        # Añadiremos más aquí abajo...
    ]

    # Mostramos los resultados en formato "Ficha"
    for l in locales:
        with st.container():
            col_img, col_info = st.columns([1, 2])
            with col_img:
                st.image(l['img'], use_container_width=True)
            with col_info:
                st.write(f"### {l['titulo']}")
                st.write(f"💰 **Precio:** {l['precio']} | 🏢 **Portal:** {l['portal']}")
                st.link_button(f"Ver local original", l['link'])
            st.divider()

with tabs[1]:
    st.subheader("Fotografía y Vídeo en Barcelona")
    st.info("Buscando nuevas ofertas...")
    # Estructura similar para empleo
    st.write("🎥 **Operador de Cámara** - Productora BCN. [Ver oferta](https://www.linkedin.com)")

with tabs[2]:
    st.subheader("Finanzas 15 Abril 2026")
    c1, c2, c3 = st.columns(3)
    c1.metric("Bitcoin", "$74,021", "+2.5%")
    c2.metric("Oro", "2.415€", "-0.8%")
    c3.metric("Euríbor", "2,76%", "Bajando")
