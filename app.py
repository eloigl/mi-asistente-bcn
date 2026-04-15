import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Premium", layout="wide")

# ESTILO CSS (Precios azul, tarjetas con sombra y tablas limpias)
st.markdown("""
    <style>
    /* Precios en Azul Profesional */
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    
    /* Cajas de Tendencia */
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    
    /* Fichas Inmuebles e Inmuebles */
    .house-card, .job-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        color: #000000;
    }
    .house-card { border-top: 5px solid #1e40af; }
    .price-tag { color: #1e40af; font-size: 1.4rem; font-weight: bold; }
    .area-tag { background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Radar BCN Premium")
st.write(f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles (Top 10)", "💼 Empleo", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    st.header("📍 Últimas Oportunidades < 150.000€")
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
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><span class="area-tag">{casa["zona"]}</span><div style="margin-top:10px;"><b>{casa["tipo"]}</b></div><div class="price-tag">{casa["precio"]}</div><div style="font-size:0.9rem; color:#444;">{casa["m2"]} | {casa["ref"]}</div></div>', unsafe_allow_html=True)
            st.link_button(f"Ver en Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/")

# --- TAB 2: EMPLEO ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛠️ Freelance")
        for t, p in [("Fotógrafo Inmuebles", "60€/s"), ("Editor Reels", "Proyecto"), ("Cámara Eventos", "250€/d"), ("Retocador Freelance", "Factura"), ("Operador Dron", "A conv.")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #16a34a;"><b>{t}</b><br>Pago: {p}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://es.indeed.com", key=t+"_f")
    with c2:
        st.subheader("👔 Contrato")
        for t, s in [("Videógrafo Content", "25k-30k"), ("Fotógrafo Producto", "Jornada"), ("Ayudante Cámara", "Convenio"), ("Editor Post-Prod", "24k"), ("Técnico AV", "22k")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #2563eb;"><b>{t}</b><br>Sueldo: {s}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS ---
with tabs[2]:
    st.header("Análisis de Mercado")
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

    # --- PARTE DE FINANCIACIÓN Y AHORRO ---
    st.subheader("🏦 Financiación y Ahorro")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("**Coste del Dinero (Préstamos)**")
        df_p = pd.DataFrame({
            "Tipo": ["Hipoteca Fija", "Hipoteca Var.", "P. Personal", "P. Coche"],
            "TAE": ["2.20%", "Euríbor+0.45%", "6.50%", "5.90%"]
        })
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    with c_b:
        st.write("**Rentabilidad (Ahorro)**")
        df_a = pd.DataFrame({
            "Producto": ["Depósito Raisin", "Cuenta Remun.", "Letras Tesoro", "Banca Tradic."],
            "Paga": ["2.85%", "2.10%", "3.15%", "0.75%"]
        })
        st.dataframe(df_a, use_container_width=True, hide_index=True)
