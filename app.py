import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Asistente BCN", layout="wide")

# Estilo para tarjetas de trabajo
st.markdown("""
    <style>
    .job-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid #FF4B4B;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .freelance-tag {
        background-color: #E1F5FE;
        color: #01579B;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 0.8em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v5.0")

tabs = st.tabs(["🏠 Inmuebles", "💼 Trabajo Filtrado", "📊 Finanzas"])

# --- TAB 1: INMUEBLES (IDEALISTA) ---
with tabs[0]:
    st.header("Locales BCN < 150k€")
    url_idealista = "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc"
    st.components.v1.iframe(url_idealista, height=600, scrolling=True)

# --- TAB 2: TRABAJO (FILTRADO FREELANCE vs CONTRATO) ---
with tabs[1]:
    st.header("Ofertas de Foto y Vídeo")
    if st.button("🔄 Refrescar y Filtrar Autónomos"):
        st.toast("Buscando ofertas para autónomos...")
    
    col_free, col_cont = st.columns(2)
    
    with col_free:
        st.subheader("🛠️ Solo FREELANCE / AUTÓNOMO")
        # Aquí la app filtraría por palabras clave como "Autónomo", "Freelance", "Project-based"
        ofertas_f = [
            {"puesto": "Fotógrafo Inmobiliario (Autónomo)", "empresa": "Tecnocasa BCN", "pago": "Por sesión", "fecha": "Hoy"},
            {"puesto": "Editor de Vídeo Reels (Freelance)", "empresa": "Influencer Agency", "pago": "300€/proyecto", "fecha": "Hace 3h"},
            {"puesto": "Cámara Evento Corporativo", "empresa": "Hotel Arts", "pago": "Factura", "fecha": "Ayer"}
        ]
        for o in ofertas_f:
            st.markdown(f"""
                <div class="job-card" style="border-left-color: #00C853;">
                    <span class="freelance-tag">AUTÓNOMO</span>
                    <h4 style="margin:5px 0;">{o['puesto']}</h4>
                    <p style="margin:0; color:#666;">{o['empresa']} • {o['pago']}</p>
                    <small>🕒 {o['fecha']}</small>
                </div>
            """, unsafe_allow_html=True)

    with col_cont:
        st.subheader("👔 Contrato Plantilla")
        ofertas_c = [
            {"puesto": "Retocador Digital Senior", "empresa": "Mango / Inditex", "sueldo": "28k - 35k", "fecha": "Hoy"},
            {"puesto": "Videógrafo Social Media", "empresa": "Startup BCN", "sueldo": "Jornada Completa", "fecha": "Ayer"}
        ]
        for o in ofertas_c:
            st.markdown(f"""
                <div class="job-card">
                    <h4 style="margin:5px 0;">{o['puesto']}</h4>
                    <p style="margin:0; color:#666;">{o['empresa']} • {o['sueldo']}</p>
                    <small>🕒 {o['fecha']}</small>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 3: FINANZAS (TODOS LOS DATOS) ---
with tabs[2]:
    st.header("📊 Mercados y Bancos (Abril 2026)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Bitcoin (BTC)", "$74.021", "+2.5%")
    c2.metric("Oro (oz)", "2.415,50 €", "-0.8%")
    c3.metric("Euríbor", "2,76%", "Bajando")
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Hipotecas y Préstamos**")
        st.table(pd.DataFrame({
            "Producto": ["Euríbor 12m", "Hipotecas Fijas", "Préstamo Personal"],
            "Hoy": ["2,76%", "2,20% TAE", "5,5% - 8%"]
        }))
    with col_b:
        st.write("**Rentabilidad Ahorro**")
        st.table(pd.DataFrame({
            "Tipo": ["Depósitos (Raisin)", "Cuentas Remuneradas", "Banca Tradicional"],
            "Pagan": ["2,85% TAE", "2,10% TAE", "0,75% TAE"]
        }))
