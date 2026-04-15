import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Premium", layout="wide")

# ESTILO CSS (Precios azul, tarjetas con sombra y texto claro)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    
    /* Estilo Fichas Inmuebles */
    .house-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-top: 5px solid #1e40af;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #000000;
    }
    .price-tag { color: #1e40af; font-size: 1.4rem; font-weight: bold; }
    .area-tag { background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Radar BCN Premium")

tabs = st.tabs(["🏠 Inmuebles (Top 10)", "💼 Empleo", "📈 Finanzas"])

# --- TAB 1: INMUEBLES (LOS 10 ELEGIDOS) ---
with tabs[0]:
    st.header("📍 Últimas Oportunidades < 150.000€")
    st.info("Filtro activo: Barcelona Capital | Recién publicados | Sin incidencias graves")
    
    # Lista de 10 locales/oficinas (Estructura preparada para actualizarse)
    inmuebles = [
        {"zona": "Eixample Esquerra", "tipo": "Local Comercial", "precio": "115.000€", "m2": "45m²", "ref": "Bajo con escaparate"},
        {"zona": "Poblenou", "tipo": "Oficina Loft", "precio": "139.000€", "m2": "55m²", "ref": "Cerca de zona tecnológica"},
        {"zona": "Sants", "tipo": "Local/Estudio", "precio": "89.000€", "m2": "38m²", "ref": "Ideal inversión"},
        {"zona": "Ciutat Vella", "tipo": "Local Histórico", "precio": "145.000€", "m2": "60m²", "ref": "Zona de alto paso"},
        {"zona": "Gràcia", "tipo": "Despacho Profesional", "precio": "120.000€", "m2": "42m²", "ref": "Exterior, mucha luz"},
        {"zona": "Sant Martí", "tipo": "Local diáfano", "precio": "95.000€", "m2": "50m²", "ref": "Recién reformado"},
        {"zona": "Les Corts", "tipo": "Oficina planta baja", "precio": "130.000€", "m2": "48m²", "ref": "Cerca de Av. Madrid"},
        {"zona": "Sagrada Família", "tipo": "Local pequeño", "precio": "75.000€", "m2": "30m²", "ref": "Oportunidad por precio"},
        {"zona": "Horta", "tipo": "Local comercial", "precio": "110.000€", "m2": "65m²", "ref": "Gran fachada"},
        {"zona": "Poble Sec", "tipo": "Estudio/Local", "precio": "99.000€", "m2": "40m²", "ref": "A 2 min del Metro"}
    ]
    
    # Mostrar en cuadrícula de 2 en 2 para que se vea bien en móvil
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="house-card">
                    <span class="area-tag">{casa['zona']}</span>
                    <div style="margin-top:10px;"><b>{casa['tipo']}</b></div>
                    <div class="price-tag">{casa['precio']}</div>
                    <div style="font-size:0.9rem; color:#444;">{casa['m2']} | {casa['ref']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.link_button(f"Ver en Idealista", f"https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc")

# --- TAB 2: EMPLEO (Mínimo 5 por columna) ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛠️ Freelance")
        for t, p in [("Fotógrafo Inmobiliario", "60€/s"), ("Editor Reels", "Proyecto"), ("Cámara Eventos", "250€/d"), ("Retocador Freelance", "Factura"), ("Operador Dron", "A conv.")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #16a34a; background:white; padding:15px; border-radius:10px; margin-bottom:10px; color:black; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><b>{t}</b><br>Pago: {p}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://es.indeed.com", key=t+"_f")
    with c2:
        st.subheader("👔 Contrato")
        for t, s in [("Videógrafo Content", "25k-30k"), ("Fotógrafo Producto", "Jornada"), ("Ayudante Cámara", "Convenio"), ("Editor Post-Prod", "24k"), ("Técnico AV", "22k")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #2563eb; background:white; padding:15px; border-radius:10px; margin-bottom:10px; color:black; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><b>{t}</b><br>Sueldo: {s}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS ---
with tabs[2]:
    def card_financiera(titulo, precio, d24, d15, m3):
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Precio / 24h", precio, d24)
        def get_class(val): return "pos-box" if "+" in val else "neg-box"
        col2.markdown(f'<div class="trend-box {get_class(d15)}"><div style="font-size:0.8rem;">15 DÍAS</div><div style="font-size:1.4rem; font-weight:800;">{d15}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_class(m3)}"><div style="font-size:0.8rem;">3 MESES</div><div style="font-size:1.4rem; font-weight:800;">{m3}</div></div>', unsafe_allow_html=True)
        st.divider()

    card_financiera("₿ Bitcoin (BTC)", "$74.021", "+2.5%", "+12.4%", "+45.0%")
    card_financiera("✨ Oro (XAU)", "2.415,50 €", "-0.8%", "+3.2%", "+8.7%")
    card_financiera("📉 Euríbor 12m", "2,767%", "-0.01%", "-0.12%", "-0.45%")
    card_financiera("🇺🇸 S&P 500", "5.210 pts", "+0.1%", "-1.5%", "+10.2%")
