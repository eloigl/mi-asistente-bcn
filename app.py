import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Radar BCN", layout="wide")

# Estilo para tarjetas y métricas
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; border: 1px solid #ddd; padding: 15px; border-radius: 12px; }
    .job-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border-left: 8px solid #007BFF; margin-bottom: 15px; color: #000000; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    .freelance-card { border-left-color: #28a745; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v8.0")
st.write(f"Última actualización: {datetime.now().strftime('%H:%Mh')}")

tabs = st.tabs(["🏠 Idealista", "💼 Trabajo", "📊 Finanzas Pro"])

# --- TAB 1: IDEALISTA ---
with tabs[0]:
    st.components.v1.iframe("https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc", height=700, scrolling=True)

# --- TAB 2: TRABAJO (Mínimo 5 por columna) ---
with tabs[1]:
    col_free, col_cont = st.columns(2)
    with col_free:
        st.subheader("🛠️ Autónomos")
        free_jobs = [
            {"t": "Fotógrafo Inmobiliario", "e": "InmoBCN", "p": "60€/sesión", "l": "https://es.indeed.com/jobs?q=fotografo+autonomo&l=Barcelona"},
            {"t": "Editor Vídeo Reels", "e": "Social Agency", "p": "Proyecto", "l": "https://www.domestika.org/es/jobs"},
            {"t": "Cámara Eventos", "e": "Productora X", "p": "250€/día", "l": "https://www.linkedin.com"},
            {"t": "Retocador Freelance", "e": "Estudio Moda", "p": "Factura", "l": "https://www.infojobs.net"},
            {"t": "Operador Dron", "e": "Constructora", "p": "A convenir", "l": "https://www.google.com/search?q=empleo+dron+barcelona"}
        ]
        for j in free_jobs:
            st.markdown(f'<div class="job-card freelance-card"><b>{j["t"]}</b><br>{j["e"]} | {j["p"]}</div>', unsafe_allow_html=True)
            st.link_button("Ver oferta", j["l"], key=j["t"])

    with col_cont:
        st.subheader("👔 Contrato")
        cont_jobs = [
            {"t": "Videógrafo Content Creator", "e": "Startup BCN", "s": "25k-30k", "l": "https://www.infojobs.net"},
            {"t": "Fotógrafo Producto", "e": "Ecommerce S.A.", "s": "Jornada Compl.", "l": "https://www.linkedin.com"},
            {"t": "Ayudante Cámara", "e": "TV Local", "s": "Convenio", "l": "https://es.indeed.com"},
            {"t": "Editor Post-Producción", "e": "Agencia Publi", "s": "24.000€", "l": "https://www.google.com"},
            {"t": "Técnico Audiovisual", "e": "Eventos BCN", "s": "22.000€", "l": "https://www.infojobs.net"}
        ]
        for j in cont_jobs:
            st.markdown(f'<div class="job-card"><b>{j["t"]}</b><br>{j["e"]} | {j["s"]}</div>', unsafe_allow_html=True)
            st.link_button("Ver oferta", j["l"], key=j["t"])

# --- TAB 3: FINANZAS PRO (CON HISTORIAL) ---
with tabs[2]:
    st.header("📈 Mercados: Tendencia y Porcentajes")
    
    # Creamos una tabla comparativa para que sea fácil de leer
    data_mercados = {
        "Activo": ["Bitcoin (BTC)", "Oro (XAU)", "S&P 500", "Euríbor 12m"],
        "Precio Actual": ["$74.021", "2.415,50 €", "5.210 pts", "2,767%"],
        "Var. 24h": ["+2,5%", "-0,8%", "+0,1%", "-0,01%"],
        "Var. 15 días": ["+12,4%", "+3,2%", "-1,5%", "-0,12%"],
        "Var. 3 meses": ["+45,0%", "+8,7%", "+10,2%", "-0,45%"]
    }
    
    st.table(pd.DataFrame(data_mercados))
    
    st.divider()
    
    st.subheader("🏦 Tipos de Interés y Ahorro")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Hipotecas y Préstamos**")
        st.table(pd.DataFrame({
            "Producto": ["Euríbor 12m", "Hipotecas Fijas", "Hipotecas Var.", "Préstamo Pers."],
            "Hoy": ["2,76%", "2,20% TAE", "E + 0,45%", "6,5% TAE"]
        }))
    with c2:
        st.write("**Rentabilidad Ahorro**")
        st.table(pd.DataFrame({
            "Depósitos": ["Raisin (Mejor)", "Cuentas Remun.", "Bancos Tradic."],
            "Pagan": ["2,85% TAE", "2,10% TAE", "0,75% TAE"]
        }))
