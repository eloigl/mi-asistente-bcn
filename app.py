import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Asistente BCN", layout="wide")

# Estilo para mejorar la visualización en móvil
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #004687; color: white; }
    iframe { border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v2.0")
st.write(f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Trabajo", "📊 Finanzas"])

# --- TAB 1: INMUEBLES (VISUALIZACIÓN DIRECTA) ---
with tabs[0]:
    st.header("Locales y Oficinas BCN")
    st.write("Selecciona el portal para ver los resultados aquí abajo:")
    
    opcion = st.radio("Elige portal:", ["Idealista", "Habitaclia", "Fotocasa"], horizontal=True)
    
    # Diccionario de links corregidos (URLs de búsqueda limpia)
    urls = {
        "Idealista": "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/",
        "Habitaclia": "https://www.habitaclia.com/venta-locales_comerciales-barcelona-hasta_150000.htm",
        "Fotocasa": "https://www.fotocasa.es/es/comprar/locales/barcelona-capital/l?maxPrice=150000"
    }

    # Intentar mostrar la web dentro de la App
    st.info(f"Mostrando resultados de {opcion} < 150k€")
    
    # Creamos una ventana (Iframe) para ver la web sin salir de la app
    # Nota: Algunos portales pueden bloquear el embebido por seguridad, 
    # si sale en blanco, el botón inferior es el plan B.
    st.components.v1.iframe(urls[opcion], height=600, scrolling=True)
    
    st.link_button(f"Abrir {opcion} en pantalla completa", urls[opcion])

    st.divider()
    st.warning("⚠️ Recuerda filtrar manualmente por 'Fecha: más recientes' si el portal no lo hace por defecto.")

# --- TAB 2: TRABAJO (FOTO & VIDEO) ---
with tabs[1]:
    st.header("📸 Fotografía y Vídeo")
    col_job1, col_job2 = st.columns(2)
    
    with col_job1:
        st.subheader("Vídeo")
        st.link_button("Ver ofertas Video BCN", "https://es.indeed.com/jobs?q=video&l=Barcelona&sort=date")
    
    with col_job2:
        st.subheader("Fotografía")
        st.link_button("Ver ofertas Foto BCN", "https://es.indeed.com/jobs?q=fotografo&l=Barcelona&sort=date")

# --- TAB 3: FINANZAS COMPLETAS (MERCADOS Y BANCOS) ---
with tabs[2]:
    st.header("📈 Mercados y 🏦 Bancos")
    
    # Fila 1: Mercados
    m1, m2, m3 = st.columns(3)
    m1.metric("Bitcoin (BTC)", "$74.021", "+2.5%")
    m2.metric("Oro (oz)", "2.415€", "-0.8%")
    m3.metric("S&P 500", "5.210 pts", "+0.1%")
    
    st.divider()
    
    # Fila 2: Tipos de Interés España
    st.subheader("Tipos de Interés y Préstamos")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**Crédito e Hipotecas**")
        st.table(pd.DataFrame({
            "Producto": ["Euríbor 12m", "Hipotecas Fijas", "Hipotecas Var.", "Préstamos"],
            "Hoy": ["2,76%", "2,20% TAE", "E+0,45%", "5,5% - 8%"]
        }))
        
    with c2:
        st.write("**Rentabilidad Ahorro**")
        st.table(pd.DataFrame({
            "Tipo": ["Depósitos (Raisin)", "Banca Tradicional", "Cuentas Remuneradas"],
            "Hoy": ["2,85% TAE", "0,75% TAE", "2,10% TAE"]
        }))
