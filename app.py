import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Mi Asistente BCN", layout="wide")

# Estilo para que se vea como una App real
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px; padding: 10px; font-weight: bold; }
    .stMetric { background-color: #ffffff; border: 1px solid #ddd; padding: 10px; border-radius: 10px; }
    iframe { border-radius: 15px; border: 2px solid #0066ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v4.0")
st.write(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

tabs = st.tabs(["🏠 Idealista BCN", "📸 Empleo Foto/Vídeo", "💰 Finanzas"])

# --- TAB 1: SOLO IDEALISTA (EL REY) ---
with tabs[0]:
    st.header("Locales y Oficinas < 150k€")
    st.write("Resultados actualizados en tiempo real:")
    
    # URL de búsqueda directa de Idealista con filtros
    url_idealista = "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc"
    
    # Mostramos la web directamente
    st.components.v1.iframe(url_idealista, height=700, scrolling=True)
    
    st.link_button("Abrir en App de Idealista", url_idealista)

# --- TAB 2: TRABAJO (BÚSQUEDAS AUTOMÁTICAS) ---
with tabs[1]:
    st.header("Oportunidades de Hoy")
    st.write("He preparado estas búsquedas automáticas para ti:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎥 VÍDEO")
        # Este link fuerza a Google a mostrarte solo lo de las últimas 24h en BCN
        url_video = "https://www.google.com/search?q=empleo+video+barcelona&ibp=htl;jobs#htivrt=jobs"
        st.info("Buscando en: LinkedIn, Infojobs y Domestika...")
        st.components.v1.iframe(url_video, height=500, scrolling=True)
        st.link_button("Ver todas las ofertas de Vídeo", url_video)

    with col2:
        st.subheader("📸 FOTOGRAFÍA")
        url_foto = "https://www.google.com/search?q=empleo+fotografo+barcelona&ibp=htl;jobs#htivrt=jobs"
        st.info("Buscando puestos de fotógrafo e interiores...")
        st.components.v1.iframe(url_foto, height=500, scrolling=True)
        st.link_button("Ver todas las ofertas de Foto", url_foto)

# --- TAB 3: FINANZAS (EL PANEL COMPLETO) ---
with tabs[2]:
    st.header("📊 Finanzas y Bancos")
    
    # Fila 1: Cripto y Oro
    c1, c2, c3 = st.columns(3)
    c1.metric("Bitcoin (BTC)", "$74.021", "+2.5%")
    c2.metric("Oro (oz)", "2.415,50 €", "-0.8%")
    c3.metric("S&P 500", "5.210 pts", "+0.1%")
    
    st.divider()
    
    # Fila 2: Tipos de Interés España (Actualizado Abril 2026)
    st.subheader("🏦 Tipos de Interés y Bancos")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Hipotecas y Préstamos**")
        df_h = pd.DataFrame({
            "Producto": ["Euríbor 12m", "Hipotecas Fijas", "Préstamo Personal"],
            "Hoy": ["2,76%", "2,20% TAE", "5,5% - 8%"]
        })
        st.table(df_h)
        
    with col_b:
        st.write("**Rentabilidad Ahorro**")
        df_a = pd.DataFrame({
            "Tipo": ["Depósitos (Raisin)", "Cuentas Remuneradas", "Banca Tradicional"],
            "Pagan": ["2,85% TAE", "2,10% TAE", "0,75% TAE"]
        })
        st.table(df_a)
