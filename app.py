import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Radar BCN", layout="wide")

# Estilo para priorizar el precio grande y texto negro
st.markdown("""
    <style>
    /* Precio principal grande */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }
    /* Etiquetas de tiempo más pequeñas */
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #444444 !important;
    }
    .stMetric { 
        background-color: #ffffff; 
        border: 1px solid #eeeeee; 
        padding: 10px; 
        border-radius: 12px; 
    }
    .job-card { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 12px; 
        border-left: 8px solid #007BFF; 
        margin-bottom: 10px; 
        color: #000000; 
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1); 
    }
    .freelance-card { border-left-color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v10.0")

tabs = st.tabs(["🏠 Idealista", "💼 Trabajo", "📊 Finanzas"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    st.components.v1.iframe("https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc", height=700, scrolling=True)

# --- TAB 2: TRABAJO ---
with tabs[1]:
    col_free, col_cont = st.columns(2)
    with col_free:
        st.subheader("🛠️ Freelance")
        jobs_f = [("Fotógrafo Inmuebles", "60€/s"), ("Editor Reels", "Proyecto"), ("Cámara Eventos", "250€/d"), ("Retocador Freelance", "Factura"), ("Operador Dron", "A conv.")]
        for t, p in jobs_f:
            st.markdown(f'<div class="job-card freelance-card"><b>{t}</b><br>Pago: {p}</div>', unsafe_allow_html=True)
            st.link_button(f"Ver {t}", "https://es.indeed.com/jobs?q=fotografo+autonomo&l=Barcelona", key=t)
    with col_cont:
        st.subheader("👔 Contrato")
        jobs_c = [("Videógrafo Content", "25k-30k"), ("Fotógrafo Producto", "Jornada"), ("Ayudante Cámara", "Convenio"), ("Editor Post-Prod", "24.000€"), ("Técnico Audiovisual", "22.000€")]
        for t, s in jobs_c:
            st.markdown(f'<div class="job-card"><b>{t}</b><br>Sueldo: {s}</div>', unsafe_allow_html=True)
            st.link_button(f"Ver {t}", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS (PRECIO GRANDE Y TIEMPOS) ---
with tabs[2]:
    st.header("📈 Mercados y Tendencias")

    def seccion_activo(titulo, precio, d24, d15, m3):
        st.write(f"### {titulo}")
        c1, c2, c3 = st.columns(3)
        # El precio actual va en el Label para que se vea arriba y grande, el cambio en el delta
        c1.metric(label="Precio Actual / 24h", value=precio, delta=d24)
        c2.metric(label="Tendencia 15 Días", value=d15, delta=None) # Aquí solo el porcentaje
        c3.metric(label="Histórico 3 Meses", value=m3, delta=None)
        st.divider()

    seccion_activo("₿ Bitcoin (BTC)", "$74.021", "+2.5%", "+12.4%", "+45.0%")
    seccion_activo("✨ Oro (XAU)", "2.415,50 €", "-0.8%", "+3.2%", "+8.7%")
    seccion_activo("📉 Euríbor 12m", "2,767%", "-0.01%", "-0.12%", "-0.45%")
    seccion_activo("🇺🇸 S&P 500", "5.210 pts", "+0.1%", "-1.5%", "+10.2%")

    st.subheader("🏦 Resumen Bancos")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Préstamos**")
        st.table(pd.DataFrame({"Tipo": ["Fijo", "Variable", "Personal"], "TAE": ["2,20%", "E+0,45%", "6,5%"]}))
    with col_b:
        st.write("**Ahorro**")
        st.table(pd.DataFrame({"Depósito": ["Raisin", "Cuenta Rem.", "Tradicional"], "Paga": ["2,85%", "2,10%", "0,75%"]}))
