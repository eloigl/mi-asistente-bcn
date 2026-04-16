import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Vivo", layout="wide")

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    .house-card, .job-card { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; color: #000000; }
    .house-card { border-top: 5px solid #1e40af; }
    .price-tag { color: #1e40af; font-size: 1.4rem; font-weight: bold; }
    .area-tag { background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN DE AUTOMATIZACIÓN FINANCIERA
def get_live_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if df.empty or len(df) < 65:
            return "Cargando...", "0%", "0%", "0%"
        actual = float(df['Close'].iloc[-1])
        ayer = float(df['Close'].iloc[-2])
        hace_15d = float(df['Close'].iloc[-11])
        hace_3m = float(df['Close'].iloc[-63])
        v24h, v15d, v3m = ((actual-ayer)/ayer)*100, ((actual-hace_15d)/hace_15d)*100, ((actual-hace_3m)/hace_3m)*100
        return f"{actual:,.2f}", f"{v24h:+.2f}%", f"{v15d:+.2f}%", f"{v3m:+.2f}%"
    except:
        return "Sincronizando...", "0%", "0%", "0%"

st.title("🚀 Radar BCN Premium v12.2")
st.write(f"Sincronización activa: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles (Top 10)", "💼 Empleo", "📈 Finanzas REAL TIME"])

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
            # ESTA ES LA LÍNEA QUE DABA EL ERROR, YA ESTÁ CERRADA:
            st.link_button(f"Ver en Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/", key=f"btn_{i}")

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
    st.header("📈 Análisis de Mercado (Live)")
    with st.spinner('Actualizando cotizaciones...'):
        btc_p, btc_24, btc_15, btc_3m = get_live_data("BTC-USD")
        oro_p, oro_24, oro_15, oro_3m = get_live_data("GC=F")
        sp_p, sp_24, sp_15, sp_3m = get_live_data("^GSPC")

    def card_financiera(titulo, precio, d24, d15, m3):
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Precio Actual", precio, d24)
        def get_class(val): return "pos-box" if "+" in val else "neg-box"
        col2.markdown(f'<div class="trend-box {get_class(d15)}"><div style="font-size:0.8rem;">15 DÍAS</div><div style="font-size:1.4rem; font-weight:800;">{d15}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_class(m3)}"><div style="font-size:0.8rem;">3 MESES</div><div style="font-size:1.4rem; font-weight:800;">{m3}</div></div>', unsafe_allow_html=True)
        st.divider()

    card_financiera("₿ Bitcoin (USD)", f"${btc_p}", btc_24, btc_15, btc_3m)
    card_financiera("✨ Oro (Onza)", f"{oro_p} €", oro_24, oro_15, oro_3m)
    card_financiera("🇺🇸 S&P 500 (Bolsa)", f"{sp_p} pts", sp_24, sp_15, sp_3m)

    st.subheader("🏦 Financiación y Ahorro")
    c_a, c_b = st.columns(2)
    with c_a:
        st.dataframe(pd.DataFrame({"Préstamos": ["Hip. Fija", "P. Personal"], "TAE": ["2.20%", "6.50%"]}), use_container_width=True, hide_index=True)
    with c_b:
        st.dataframe(pd.DataFrame({"Ahorro": ["Raisin", "Letras Tesoro"], "Paga": ["2.85%", "3.15%"]}), use_container_width=True, hide_index=True)
