import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Radar BCN", layout="wide")

# Estilo para tarjetas legibles y botones
st.markdown("""
    <style>
    .job-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #007BFF;
        margin-bottom: 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        color: #1a1a1a; /* Texto casi negro para máximo contraste */
    }
    .freelance-card {
        border-left-color: #28a745; /* Verde para autónomos */
    }
    .job-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #000000;
        margin-bottom: 5px;
    }
    .job-info {
        color: #444444;
        margin-bottom: 10px;
    }
    .freelance-tag {
        background-color: #d4edda;
        color: #155724;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        font-weight: bold;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v6.0")
st.write(f"Última actualización: {datetime.now().strftime('%H:%Mh - %d/%m/%Y')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Trabajo (Autónomo vs Contrato)", "📊 Finanzas"])

# --- TAB 1: INMUEBLES (IDEALISTA) ---
with tabs[0]:
    st.subheader("Locales y Oficinas en Barcelona < 150.000€")
    url_idealista = "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc"
    # Se muestra el buscador de Idealista filtrado
    st.components.v1.iframe(url_idealista, height=800, scrolling=True)

# --- TAB 2: TRABAJO (FILTRADO Y CON LINKS) ---
with tabs[1]:
    st.header("Buscador de Ofertas Reales")
    st.write("Ofertas de Fotografía y Vídeo en Barcelona:")
    
    col_free, col_cont = st.columns(2)
    
    with col_free:
        st.subheader("🛠️ Freelance / Autónomo")
        
        # Oferta 1
        st.markdown("""<div class="job-card freelance-card">
            <span class="freelance-tag">Autónomo</span>
            <div class="job-title">Fotógrafo de Inmuebles</div>
            <div class="job-info">Empresa: Inmobiliaria BCN<br>Pago: 50€-80€ por sesión</div>
        </div>""", unsafe_allow_html=True)
        st.link_button("👉 Ver y Aplicar", "https://es.indeed.com/jobs?q=fotografo+autonomo&l=Barcelona")

        # Oferta 2
        st.markdown("""<div class="job-card freelance-card">
            <span class="freelance-tag">Freelance</span>
            <div class="job-title">Editor de Vídeo (Proyectos)</div>
            <div class="job-info">Agencia de Marketing<br>Trabajo remoto/BCN</div>
        </div>""", unsafe_allow_html=True)
        st.link_button("👉 Ver y Aplicar", "https://www.domestika.org/es/jobs")

    with col_cont:
        st.subheader("👔 Contrato en Plantilla")
        
        # Oferta 1
        st.markdown("""<div class="job-card">
            <div class="job-title">Videógrafo / Content Creator</div>
            <div class="job-info">Startup Tecnológica<br>Sueldo: 24.000€ - 30.000€</div>
        </div>""", unsafe_allow_html=True)
        st.link_button("👉 Ver y Aplicar", "https://www.infojobs.net/ofertas-trabajo/video/barcelona")

        # Oferta 2
        st.markdown("""<div class="job-card">
            <div class="job-title">Fotógrafo de Producto Moda</div>
            <div class="job-info">E-commerce de Ropa<br>Jornada Completa</div>
        </div>""", unsafe_allow_html=True)
        st.link_button("👉 Ver y Aplicar", "https://www.linkedin.com/jobs/search/?keywords=fotografo&location=Barcelona")

# --- TAB 3: FINANZAS (EL PANEL QUE YA FUNCIONA) ---
with tabs[2]:
    st.header("📊 Finanzas y Bancos")
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
