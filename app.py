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

# FUNCIÓN DE AUTOMATIZACIÓN ULTRA-ROBUSTA
def get_live_data(ticker):
    try:
        # Descarga simple sin hilos ni progresos para evitar bloqueos
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period="6mo")
        
        if df.empty or len(df) < 10:
            return "---", "0%", "0%", "0%"
            
        actual = float(df['Close'].iloc[-1])
        ayer = float(df['Close'].iloc[-2])
        # Buscamos posiciones seguras hacia atrás
        hace_15d = float(df['Close'].iloc[-11]) if len(df) > 11 else ayer
        hace_3m = float(df['Close'].iloc[0])
        
        v24h = ((actual - ayer) / ayer) * 100
        v15d = ((actual - hace_15d) / hace_15d) * 100
        v3m = ((actual - hace_3m) / hace_3m) * 100
        
        return f"{actual:,.2f}", f"{v24h:+.2f}%", f"{v15d:+.2f}%", f"{v3m:+.2f}%"
    except Exception:
        return "Error Red", "0%", "0%", "0%"

st.title("🚀 Radar BCN Premium v12.3")
st.write(f"Sincronización: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo", "📈 Finanzas"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    inmuebles = [
        {"zona": "Eixample Esquerra", "tipo": "Local Comercial", "precio": "115.000€", "m2": "45m²", "ref": "Bajo con escaparate"},
        {"zona": "Poblenou", "tipo": "Oficina Loft", "precio": "139.000€", "m2": "55m²", "ref": "Cerca de zona tecnológica"},
        {"zona": "Sants", "tipo": "Local/Estudio", "precio": "89.000€", "m2": "38m²", "ref": "Ideal inversión"},
        {"zona": "Ciutat Vella", "tipo": "Local Histórico", "precio": "145.000€", "m2": "60m²", "ref": "Zona de alto paso"},
        {"zona": "Gràcia", "tipo": "Despacho Profesional", "precio": "120.000€", "m2": "42m²", "ref": "Exterior, mucha luz"}
    ]
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><span class="area-tag">{casa["zona"]}</span><div style="margin-top:10px;"><b>{casa["tipo"]}</b></div><div class="price-tag">{casa["precio"]}</div><div style="font-size:0.9rem; color:#444;">{casa["m2"]} | {casa["ref"]}</div></div>', unsafe_allow_html=True)
            st.link_button(f"Ver Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/", key=f"house_{i}")

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

# --- TAB 3: FINANZAS ---
with tabs[2]:
    st.header("📈 Análisis Live")
    
    # Lista de Tickers corregida
    tickers = {"₿ Bitcoin": "BTC-USD", "✨ Oro": "GC=F", "🇺🇸 S&P 500": "^GSPC"}
    
    for nombre, tick in tickers.items():
        p, d24, d15, m3 = get_live_data(tick)
        st.markdown(f"### {nombre}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Precio", p, d24)
        def get_cl(v): return "pos-box" if "+" in v else "neg-box"
        col2.markdown(f'<div class="trend-box {get_cl(d15)}"><div style="font-size:0.8rem;">15D</div><div style="font-size:1.2rem; font-weight:800;">{d15}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_cl(m3)}"><div style="font-size:0.8rem;">3M</div><div style="font-size:1.2rem; font-weight:800;">{m3}</div></div>', unsafe_allow_html=True)
        st.divider()
