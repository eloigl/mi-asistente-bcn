import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Ultra v16.4", layout="wide")

# ESTILO CSS (RESTAURADO Y CORREGIDO)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    
    /* Cajas de tendencias (Diseño original recuperado) */
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7 !important; color: #14532d !important; }
    .neg-box { background-color: #fee2e2 !important; color: #7f1d1d !important; }
    
    /* Tarjetas de Empleo y Contraste */
    .job-board-card {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
    .job-title { color: #1e3a8a !important; font-weight: 800; font-size: 1.3rem; }
    
    /* FORZAR LETRAS BLANCAS EN BOTONES */
    .stButton>button {
        color: white !important;
        background-color: #1e40af !important;
        font-weight: bold !important;
    }

    .job-tag {
        font-size: 0.75rem;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        color: white !important;
        display: inline-block;
        margin-bottom: 12px;
    }
    .tag-indeed { background-color: #2557a7 !important; }
    .tag-infojobs { background-color: #ff6000 !important; }
    .tag-linkedin { background-color: #0077b5 !important; }

    .house-card { background: white !important; padding: 15px; border-radius: 12px; border-top: 5px solid #1e40af; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN FINANZAS
def get_full_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 65: return "---", "0%", "0%", "0%", 0.0
        act, ant = float(df['Close'].iloc[-1]), float(df['Close'].iloc[-2])
        h15, h3m = float(df['Close'].iloc[-11]), float(df['Close'].iloc[0])
        return f"{act:,.2f}", f"{((act-ant)/ant)*100:+.2f}%", f"{((act-h15)/h15)*100:+.2f}%", f"{((act-h3m)/h3m)*100:+.2f}%", act
    except: return "Error", "0%", "0%", "0%", 0.0

# HEADER Y TITULO RECUPERADO
ahora = datetime.now().strftime('%d/%m/%Y | %H:%M:%S')
st.title("🚀 Radar BCN Ultra v16.4")
st.info(f"Última actualización global: {ahora} (Sincronización cada 12h)")

tabs = st.tabs(["🏠 Inmuebles", "💼 TABLÓN DE EMPLEO", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    inmuebles = [
        {"z": "Eixample", "t": "Local Comercial", "p": "115.000€"},
        {"z": "Poblenou", "t": "Oficina Loft", "p": "139.000€"},
        {"z": "Sants", "t": "Local/Estudio", "p": "89.000€"},
        {"z": "Ciutat Vella", "t": "Local Histórico", "p": "145.000€"}
    ]
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><b style="color:#1e3a8a">{casa["t"]}</b><br>{casa["z"]} | <span style="color:#1e40af; font-weight:bold">{casa["p"]}</span></div>', unsafe_allow_html=True)
            st.link_button("Ver en Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/", key=f"id_{i}")

# --- TAB 2: EMPLEO (8 PUESTOS) ---
with tabs[1]:
    puestos = [
        {"t": "Fotógrafo de Inmuebles", "p": "Indeed", "tag": "tag-indeed"},
        {"t": "Videógrafo / Editor Reels", "p": "InfoJobs", "tag": "tag-infojobs"},
        {"t": "Técnico Audiovisual", "p": "LinkedIn", "tag": "tag-linkedin"},
        {"t": "Content Creator Digital", "p": "Indeed", "tag": "tag-indeed"},
        {"t": "Editor de Vídeo YouTube", "p": "InfoJobs", "tag": "tag-infojobs"},
        {"t": "Operador de Cámara", "p": "LinkedIn", "tag": "tag-linkedin"},
        {"t": "Ayudante de Producción", "p": "Indeed", "tag": "tag-indeed"},
        {"t": "Social Media Video", "p": "InfoJobs", "tag": "tag-infojobs"}
    ]
    c1, c2 = st.columns(2)
    for i, job in enumerate(puestos):
        target = c1 if i % 2 == 0 else c2
        with target:
            st.markdown(f"""<div class="job-board-card"><span class="job-tag {job['tag']}">{job['p']}</span><div class="job-title">{job['t']}</div><div style="color: #475569; font-size: 0.85rem;">Barcelona | Actualizado: {ahora}</div></div>""", unsafe_allow_html=True)
            q = job['t'].replace(" ", "+")
            url = f"https://es.indeed.com/jobs?q={q}&l=Barcelona&fromage=1" if job['p'] == "Indeed" else f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={q}" if job['p'] == "InfoJobs" else f"https://www.linkedin.com/jobs/search/?keywords={q}&location=Barcelona&f_TPR=r86400"
            st.link_button(f"VER EN {job['p'].upper()}", url, key=f"job_btn_{i}", use_container_width=True)

# --- TAB 3: FINANZAS (DISEÑO ORIGINAL RECUPERADO) ---
with tabs[2]:
    def render_card(titulo, ticker, es_moneda=True):
        p, d24, d15, m3, val_puro = get_full_data(ticker)
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        simbolo = "$" if es_moneda and "USD" in ticker else "€" if es_moneda else ""
        col1.metric("Hoy", f"{p} {simbolo}", d24)
        def get_cl(v): return "pos-box" if "+" in v else "neg-box"
        col2.markdown(f'<div class="trend-box {get_cl(d15)}"><div style="font-size:0.8rem;">15 DÍAS</div><div style="font-size:1.3rem; font-weight:800;">{d15}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_cl(m3)}"><div style="font-size:0.8rem;">3 MESES</div><div style="font-size:1.3rem; font-weight:800;">{m3}</div></div>', unsafe_allow_html=True)
        st.divider()
        return val_puro

    render_card("₿ Bitcoin", "BTC-USD")
    render_card("✨ Oro", "GC=F")
    render_card("🇺🇸 S&P 500", "^GSPC", es_moneda=False)
    irx_val = render_card("📉 Euríbor / Tipos (Ref)", "^IRX", es_moneda=False)
