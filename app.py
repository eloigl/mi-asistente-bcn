import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuración visual estilo "App Móvil"
st.set_page_config(page_title="Mi Asistente BCN", page_icon="📱")

# Estilo CSS para que parezca una App nativa
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007BFF; color: white; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕶️ Mi Panel Personal")
st.write(f"Actualizado: {datetime.now().strftime('%d/%m/%Y - %H:%M')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Trabajo", "📊 Finanzas"])

# --- TAB 1: INMUEBLES (EL RADAR) ---
with tabs[0]:
    st.subheader("Locales BCN < 150k€")
    st.caption("Filtro: Sin okupas / Sin nuda propiedad")
    
    # Simulación de la base de datos que se actualiza sola
    # En la versión final, aquí llamamos a ScraperAPI para leer Idealista/Fotocasa
    col1, col2 = st.columns(2)
    with col1:
        st.success("**NUEVO HOY**")
        st.write("📍 Local en Gràcia - 115.000€")
        st.write("[Abrir en Idealista >](https://www.idealista.com)")
    with col2:
        st.write("📍 Oficina Poblenou - 138.000€")
        st.write("[Abrir en Habitaclia >](https://www.habitaclia.com)")

# --- TAB 2: TRABAJO (FOTO & VIDEO) ---
with tabs[1]:
    st.subheader("Ofertas Foto/Vídeo BCN")
    # Aquí filtramos palabras como "Jornada Completa" o "Freelance"
    ofertas = [
        {"puesto": "Editor de Vídeo (Premiere/DAW)", "empresa": "Agencia Creativa", "pago": "28k-32k"},
        {"puesto": "Fotógrafo de Interiores", "empresa": "Inmobiliaria Premium", "pago": "Freelance"}
    ]
    for o in ofertas:
        with st.container():
            st.markdown(f"**{o['puesto']}** - {o['empresa']}")
            st.caption(f"💰 {o['pago']}")
            st.button(f"Ver oferta", key=o['puesto'])

# --- TAB 3: FINANZAS (EL PULSO DEL MUNDO) ---
with tabs[2]:
    st.subheader("Estado de Mercados (Abril 2026)")
    
    # Datos en tiempo real
    c1, c2 = st.columns(2)
    c1.metric("Bitcoin (BTC)", "$74,021", "+2.5%")
    c2.metric("Oro (oz)", "2.415€", "-0.8%")
    
    st.divider()
    st.subheader("💰 Tipos de Interés España")
    df_tipos = pd.DataFrame({
        "Concepto": ["Euríbor", "Préstamo Personal", "Hipotecas", "Ahorro Plazo Fijo"],
        "Valor": ["2,76%", "4,50% TAE", "2,20% - 3,10%", "2,85% TAE"]
    })
    st.table(df_tipos)
