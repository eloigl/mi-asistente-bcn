import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Vivo", layout="wide")

# ESTILO CSS (Precios azul, cajas de tendencia y tarjetas)
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

# FUNCIÓN DE AUTOMATIZACIÓN FINANCIERA MEJORADA
def get_live_data(ticker):
    try:
        # Descargamos 6 meses para tener margen de sobra para los cálculos
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if df.empty or len(df) < 65:
            return "Cargando...", "0%", "0%", "0%"
            
        # Extraemos valores de cierre asegurando que sean números (float)
        actual = float(df['Close'].iloc[-1])
        ayer = float(df['Close'].iloc[-2])
        # Usamos posiciones fijas en el historial para evitar errores con festivos
        hace_15d = float(df['Close'].iloc[-11]) # ~15 días naturales
        hace_3m = float(df['Close'].iloc[-63])  # ~3 meses naturales
        
        v24h = ((actual - ayer) / ayer) * 100
        v15d = ((actual - hace_15d) / hace_15d) * 100
        v3m = ((actual - hace_3m) / hace_3m) * 100
        
        return f"{actual:,.2f}", f"{v24h:+.2f}%", f"{v15d:+.2f}%", f"{v3m:+.2f}%"
    except Exception as e:
        return "Sincronizando...", "0%", "0%", "0%"

st.title("🚀 Radar BCN Premium v12.1")
st.write(f"Sincronización activa: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles (Top 10)", "💼 Empleo", "📈 Finanzas REAL TIME"])

# --- TAB 1: INMUEBLES (TOP 10) ---
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
            st.link_button(f"Ver en Idealista", "
