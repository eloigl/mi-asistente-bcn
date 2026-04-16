import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Premium", layout="wide")

# ESTILO CSS (Tu diseño azul y limpio)
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

# FUNCIÓN ÚNICA DE SINCRONIZACIÓN
def get_live_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty: return 0.0, "0%", 0.0
        actual = float(df['Close'].iloc[-1])
        ayer = float(df['Close'].iloc[-2])
        v24h = ((actual - ayer) / ayer) * 100
        return actual, f"{v24h:+.2f}%", actual
    except:
        return 0.0, "0%", 0.0

st.title("🚀 Radar BCN Premium")
st.write(f"Sincronización total: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo", "📈 Finanzas & Bancos"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    inmuebles = [
        {"zona": "Eixample Esquerra", "tipo": "Local Comercial", "precio": "115.000€", "m2": "45m²", "ref": "Bajo escaparate"},
        {"zona": "Poblenou", "tipo": "Oficina Loft", "precio": "139.000€", "m2": "55m²", "ref": "Zona tecnológica"},
        {"zona": "Sants", "tipo": "Local/Estudio", "precio": "89.000€", "m2": "38m²", "ref": "Ideal inversión"},
        {"zona": "Ciutat Vella", "tipo": "Local Histórico", "precio": "145.000€", "m2": "60m²", "ref": "Zona alto paso"},
        {"zona": "Gràcia", "tipo": "Despacho Prof.", "precio": "120.000€", "m2": "42m²", "ref": "Exterior, luz"},
        {"zona": "Sant Martí", "tipo": "Local diáfano", "precio": "95.000€", "m2": "50m²", "ref": "Reformado"},
        {"zona": "Les Corts", "tipo": "Oficina PB", "precio": "130.000€", "m2": "48m²", "ref": "Cerca Av. Madrid"},
        {"zona": "Sagrada Fam.", "tipo": "Local pequeño", "precio": "75.000€", "m2": "30m²", "ref": "Oportunidad"},
        {"zona": "Horta", "tipo": "Local comercial", "precio": "110.000€", "m2": "65m²", "ref": "Gran fachada"},
        {"zona": "Poble Sec", "tipo": "Estudio/Local", "precio": "99.000€", "m2": "40m²", "ref": "Cerca Metro"}
    ]
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><span class="area-tag">{casa["zona"]}</span><div style="margin-top:10px;"><b>{casa["tipo"]}</b></div><div class="price-tag">{casa["precio"]}</div><div style="font-size:0.9rem; color:#444;">{casa["m2"]} | {casa["ref"]}</div></div>', unsafe_allow_html=True)
            st.link_button("Ver Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/", key=f"h_{i}")

# --- TAB 2: EMPLEO ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛠️ Freelance")
        for t, p in [("Fotógrafo", "60€/s"), ("Editor Reels", "Proyecto"), ("Dron", "A conv.")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #16a34a;"><b>{t}</b><br>{p}</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("👔 Contrato")
        for t, s in [("Videógrafo", "25k"), ("Post-Prod", "24k"), ("Técnico AV", "22k")]:
            st.markdown(f'<div class="job-card" style="border-left: 6px solid #2563eb;"><b>{t}</b><br>{s}</div>', unsafe_allow_html=True)

# --- TAB 3: FINANZAS Y BANCOS (TODO AUTO) ---
with tabs[2]:
    st.header("📈 Análisis de Mercado")
    
    with st.spinner('Sincronizando con mercados...'):
        btc_p, btc_v, _ = get_live_data("BTC-USD")
        oro_p, oro_v, _ = get_live_data("GC=F")
        # Referencia para bancos: Letras a 3 meses e índice interbancario
        _, _, irx_val = get_live_data("^IRX")
        
    m1, m2 = st.columns(2)
    m1.metric("₿ Bitcoin", f"${btc_p:,.2f}", btc_v)
    m2.metric("✨ Oro", f"{oro_p:,.2f} €", oro_v)
    
    st.divider()
    st.subheader("🏦 Financiación y Ahorro Sincronizado")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Coste Préstamos**")
        # Euribor estimado basado en tipos actuales
        euribor_hoy = 3.15 
        df_p = pd.DataFrame({
            "Tipo": ["Hipoteca Fija", "Hipoteca Variable", "P. Personal"],
            "TAE": ["2.25%", f"Eur. + 0.45% ({euribor_hoy+0.45:.2f}%)", "6.75%"]
        })
        st.dataframe(df_p, use_container_width=True, hide_index=True)

    with col_b:
        st.write("**Rentabilidad Ahorro**")
        # El interés de ahorro se mueve con el índice IRX
        rent_letras = f"{irx_val - 0.25:.2f}%" if irx_val > 0 else "3.10%"
        rent_cuenta = f"{irx_val - 1.20:.2f}%" if irx_val > 0 else "2.10%"
        df_a = pd.DataFrame({
            "Producto": ["Letras Tesoro", "Cuenta Remunerada", "Raisin (Top)"],
            "Paga": [rent_letras, rent_cuenta, "3.35%"]
        })
        st.dataframe(df_a, use_container_width=True, hide_index=True)

    st.caption(f"Referencia técnica: Rendimiento deuda pública hoy en {irx_val:.2f}%")
