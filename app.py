import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Radar BCN", layout="wide")

# Estilo para que las métricas tengan buen tamaño y las tarjetas sean legibles
st.markdown("""
    <style>
    .stMetric { 
        background-color: #ffffff; 
        border: 1px solid #eeeeee; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .job-card { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 12px; 
        border-left: 8px solid #007BFF; 
        margin-bottom: 15px; 
        color: #000000; 
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1); 
    }
    .freelance-card { border-left-color: #28a745; }
    h3 { margin-top: 20px; color: #1f1f1f; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Mi Radar BCN v9.0")
st.write(f"Actualizado: {datetime.now().strftime('%H:%Mh')}")

tabs = st.tabs(["🏠 Idealista", "💼 Trabajo", "📊 Finanzas Visual"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    st.components.v1.iframe("https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc", height=700, scrolling=True)

# --- TAB 2: TRABAJO (Mínimo 5 por columna) ---
with tabs[1]:
    col_free, col_cont = st.columns(2)
    with col_free:
        st.subheader("🛠️ Autónomos")
        jobs_f = [
            ("Fotógrafo Inmuebles", "InmoBCN", "60€/s"),
            ("Editor Reels", "Social Media", "Proyecto"),
            ("Cámara Eventos", "Productora X", "250€/d"),
            ("Retocador Freelance", "Estudio Moda", "Factura"),
            ("Operador Dron", "Constructora", "A conv.")
        ]
        for t, e, p in jobs_f:
            st.markdown(f'<div class="job-card freelance-card"><b>{t}</b><br>{e} | {p}</div>', unsafe_allow_html=True)
            st.link_button(f"Ver {t}", "https://es.indeed.com/jobs?q=fotografo+autonomo&l=Barcelona", key=t)

    with col_cont:
        st.subheader("👔 Contrato")
        jobs_c = [
            ("Videógrafo Content", "Startup BCN", "25k-30k"),
            ("Fotógrafo Producto", "Ecommerce S.A.", "Jornada"),
            ("Ayudante Cámara", "TV Local", "Convenio"),
            ("Editor Post-Prod", "Agencia Publi", "24.000€"),
            ("Técnico Audiovisual", "Eventos BCN", "22.000€")
        ]
        for t, e, s in jobs_c:
            st.markdown(f'<div class="job-card"><b>{t}</b><br>{e} | {s}</div>', unsafe_allow_html=True)
            st.link_button(f"Ver {t}", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS VISUAL (CON FLECHAS Y COLORES) ---
with tabs[2]:
    st.header("📈 Evolución de Mercados")

    # Función auxiliar para crear la fila de métricas por activo
    def fila_metrica(nombre, precio, d24h, d15d, m3):
        st.subheader(nombre)
        c1, c2, c3 = st.columns(3)
        c1.metric(f"{precio}", f"Hoy (24h)", d24h)
        c2.metric(f"Tendencia", "15 Días", d15d)
        c3.metric(f"Histórico", "3 Meses", m3)
        st.divider()

    # Datos Actualizados (Simulados para el ejemplo visual)
    fila_metrica("₿ Bitcoin (BTC)", "$74.021", "+2.5%", "+12.4%", "+45.0%")
    fila_metrica("✨ Oro (XAU)", "2.415,50 €", "-0.8%", "+3.2%", "+8.7%")
    fila_metrica("📉 Euríbor 12m", "2,767%", "-0.01%", "-0.12%", "-0.45%")
    fila_metrica("🇺🇸 S&P 500", "5.210 pts", "+0.1%", "-1.5%", "+10.2%")

    st.subheader("🏦 Resumen Bancos")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Préstamos**")
        st.table(pd.DataFrame({"Tipo": ["Fijo", "Variable", "Personal"], "TAE": ["2,20%", "E+0,45%", "6,5%"]}))
    with col_b:
        st.write("**Ahorro**")
        st.table(pd.DataFrame({"Depósito": ["Raisin", "Cuenta Rem.", "Tradicional"], "Paga": ["2,85%", "2,10%", "0,75%"]}))
