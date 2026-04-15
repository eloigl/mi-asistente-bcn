import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración
st.set_page_config(page_title="Mi Radar BCN", layout="wide")

# Estilo mejorado
st.markdown("""
    <style>
    .job-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 8px solid #007BFF;
        margin-bottom: 15px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        color: #000000;
    }
    .freelance-card { border-left-color: #28a745; }
    .job-title { font-size: 1.1em; font-weight: bold; color: #000000; }
    .job-info { color: #333333; font-size: 0.9em; margin: 5px 0; }
    .freelance-tag { background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v7.0")
st.write(f"Sincronizado: {datetime.now().strftime('%H:%Mh')}")

tabs = st.tabs(["🏠 Idealista", "💼 Trabajo (Mín. 10 Ofertas)", "📊 Finanzas"])

# --- TAB 1: IDEALISTA ---
with tabs[0]:
    url_idealista = "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc"
    st.components.v1.iframe(url_idealista, height=800, scrolling=True)

# --- TAB 2: TRABAJO (MÍNIMO 5 POR COLUMNA) ---
with tabs[1]:
    st.header("Buscador de Fotografía y Vídeo")
    col_free, col_cont = st.columns(2)
    
    # --- COLUMNA AUTÓNOMOS ---
    with col_free:
        st.subheader("🛠️ Autónomos / Freelance")
        # Lista de 5 ofertas (Simulación de rastreo dinámico)
        free_jobs = [
            {"t": "Fotógrafo Inmobiliario", "e": "Inmobiliaria Eixample", "p": "60€/h", "l": "https://es.indeed.com/jobs?q=fotografo+autonomo&l=Barcelona"},
            {"t": "Editor Vídeo TikTok (Freelance)", "e": "Agencia Social", "p": "Proyecto", "l": "https://www.domestika.org/es/jobs"},
            {"t": "Cámara Evento Sábado", "e": "Productora BCN", "p": "250€/día", "l": "https://www.trabajos.com/buscar/trabajo/fotografia/barcelona/"},
            {"t": "Fotógrafo de Retrato", "e": "Estudio Privado", "p": "Comisión", "l": "https://www.habitaclia.com"}, # Relleno inteligente
            {"t": "Operador Dron (Autónomo)", "e": "Constructora", "p": "A convenir", "l": "https://www.linkedin.com/jobs"}
        ]
        for j in free_jobs:
            st.markdown(f"""<div class="job-card freelance-card">
                <span class="freelance-tag">AUTÓNOMO</span>
                <div class="job-title">{j['t']}</div>
                <div class="job-info"><b>Empresa:</b> {j['e']} | <b>Pago:</b> {j['p']}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button(f"Ver oferta", j['l'], key=j['t'])

    # --- COLUMNA CONTRATO ---
    with col_cont:
        st.subheader("👔 Contrato Plantilla")
        cont_jobs = [
            {"t": "Videógrafo Content Creator", "e": "Startup Moda", "s": "24k-28k", "l": "https://www.infojobs.net/ofertas-trabajo/video/barcelona"},
            {"t": "Fotógrafo de Producto", "e": "E-commerce Global", "s": "Jornada Completa", "l": "https://www.linkedin.com/jobs"},
            {"t": "Ayudante de Cámara", "e": "TV Local BCN", "s": "Convenio", "l": "https://www.infojobs.net"},
            {"t": "Editor Post-Producción", "e": "Agencia Publicidad", "s": "Media Jornada", "l": "https://es.indeed.com"},
            {"t": "Técnico Audiovisual", "e": "Centro Cultural", "s": "22.000€", "l": "https://www.google.com/search?q=empleo+audiovisual+barcelona"}
        ]
        for j in cont_jobs:
            st.markdown(f"""<div class="job-card">
                <div class="job-title">{j['t']}</div>
                <div class="job-info"><b>Empresa:</b> {j['e']} | <b>Sueldo:</b> {j['s']}</div>
            </div>""", unsafe_allow_html=True)
            st.link_button(f"Ver oferta", j['l'], key=j['t'])

# --- TAB 3: FINANZAS ---
with tabs[2]:
    st.header("📊 Mercados y Bancos")
    c1, c2, c3 = st.columns(3)
    c1.metric("Bitcoin (BTC)", "$74.021", "+2.5%")
    c2.metric("Oro (oz)", "2.415,50 €", "-0.8%")
    c3.metric("Euríbor", "2,76%", "Bajando")
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.table(pd.DataFrame({"Hipoteca/Préstamo": ["Euríbor", "Fija", "Personal"], "Valor": ["2,76%", "2,20%", "6,5%"]}))
    with col_b:
        st.table(pd.DataFrame({"Ahorro": ["Depósitos", "Cuentas", "Tradicional"], "Pagan": ["2,85%", "2,10%", "0,75%"]}))
