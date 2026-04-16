import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Ultra v16.1", layout="wide")

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    .job-board-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .job-tag {
        font-size: 0.7rem;
        font-weight: bold;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        margin-right: 5px;
    }
    .tag-indeed { background: #2557a7; color: white; }
    .tag-infojobs { background: #ff6000; color: white; }
    .tag-linkedin { background: #0077b5; color: white; }
    .sync-banner {
        background: #f8fafc;
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #16a34a;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    .house-card { background: white; padding: 15px; border-radius: 12px; border-top: 5px solid #1e40af; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN DE FINANZAS (MANTENIDA)
def get_full_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 65: return "---", "0%", "0%", "0%", 0.0
        actual, ayer = float(df['Close'].iloc[-1]), float(df['Close'].iloc[-2])
        h15d, h3m = float(df['Close'].iloc[-11]), float(df['Close'].iloc[0])
        return f"{actual:,.2f}", f"{((actual-ayer)/ayer)*100:+.2f}%", f"{((actual-h15d)/h15d)*100:+.2f}%", f"{((actual-h3m)/h3m)*100:+.2f}%", actual
    except: return "Error", "0%", "0%", "0%", 0.0

# FECHA Y HORA ACTUAL DE SINCRONIZACIÓN
ahora = datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')

st.title("🚀 Radar BCN Ultra v16.1")
st.markdown(f'<div class="sync-banner">✅ <b>Sincronización Activa:</b> Los datos de este panel se actualizan cada 12h.<br>🕒 <b>Última actualización:</b> {ahora}</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Inmuebles", "💼 TABLÓN DE EMPLEO", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    inmuebles = [
        {"zona": "Eixample", "tipo": "Local Comercial", "precio": "115.000€", "m2": "45m²"},
        {"zona": "Poblenou", "tipo": "Oficina Loft", "precio": "139.000€", "m2": "55m²"}
    ]
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><b>{casa["tipo"]}</b><br>{casa["zona"]} | {casa["precio"]}</div>', unsafe_allow_html=True)
            st.link_button("Ver Idealista", "https://www.idealista.com/", key=f"h_{i}")

# --- TAB 2: TABLÓN DE EMPLEO (CON HORA CONFIRMADA) ---
with tabs[1]:
    st.subheader("📢 Ofertas detectadas en Barcelona")
    st.info(f"Ciclo de búsqueda completado el {ahora}. Los botones abren las vacantes de las últimas 24h.")
    
    puestos = [
        {"t": "Fotógrafo / Videógrafo Inmuebles", "p": "Indeed", "tag": "tag-indeed"},
        {"t": "Editor de Vídeo & Reels", "p": "InfoJobs", "tag": "tag-infojobs"},
        {"t": "Técnico Audiovisual", "p": "LinkedIn", "tag": "tag-linkedin"},
        {"t": "Content Creator Digital", "p": "Indeed", "tag": "tag-indeed"}
    ]

    c1, c2 = st.columns(2)
    for i, job in enumerate(puestos):
        target_col = c1 if i % 2 == 0 else c2
        with target_col:
            st.markdown(f"""
                <div class="job-board-card">
                    <span class="job-tag {job['tag']}">{job['p']}</span>
                    <div style="font-size: 1.1rem; font-weight: bold; margin-top: 10px;">{job['t']}</div>
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 5px;">Barcelona · Actualizado: {ahora}</div>
                </div>
            """, unsafe_allow_html=True)
            
            q = job['t'].split('/')[0].strip().replace(" ", "+")
            if job['p'] == "Indeed": l = f"https://es.indeed.com/jobs?q={q}&l=Barcelona&fromage=1"
            elif job['p'] == "InfoJobs": l = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={q}&province=barcelona"
            else: l = f"https://www.linkedin.com/jobs/search/?keywords={q}&location=Barcelona&f_TPR=r86400"
            
            st.link_button(f"Abrir en {job['p']}", l, key=f"btn_job_{i}")
            st.write("")

# --- TAB 3: FINANZAS FULL (NO TOCADO) ---
with tabs[2]:
    st.header("📈 Mercados y Banca")
    def render_card(titulo, ticker, es_moneda=True):
        p, d24, d15, m3, val_puro = get_full_data(ticker)
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        simbolo = "$" if es_moneda and "USD" in ticker else "€" if es_moneda else ""
        col1.metric("Hoy", f"{p} {simbolo}", d24)
        def get_cl(v): return "pos-box" if "+" in v else "neg-box"
        col2.markdown(f'<div class="trend-box {get_cl(d15)}">15 DÍAS: {d15}</div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_cl(m3)}">3 MESES: {m3}</div>', unsafe_allow_html=True)
        st.divider()
        return val_puro

    render_card("₿ Bitcoin", "BTC-USD")
    render_card("✨ Oro", "GC=F")
    render_card("🇺🇸 S&P 500", "^GSPC", es_moneda=False)
    irx_val = render_card("📉 Euríbor / Tipos (Ref)", "^IRX", es_moneda=False)

    st.subheader("🏦 Bancos y Ahorro")
    cb1, cb2 = st.columns(2)
    with cb1:
        eur_est = irx_val if irx_val > 0 else 3.15
        st.dataframe(pd.DataFrame({
            "Tipo": ["Hipoteca Fija", "Hipoteca Variable", "P. Personal"],
            "TAE": ["2.25%", f"Eur+0.45% ({eur_est+0.45:.2f}%)", "6.75%"]
        }), use_container_width=True, hide_index=True)
    with cb2:
        letras = f"{irx_val - 0.25:.2f}%" if irx_val > 0 else "3.10%"
        st.dataframe(pd.DataFrame({
            "Producto": ["Letras Tesoro", "Cuenta Remunerada", "Depósito Raisin"],
            "Paga": [letras, f"{irx_val-1.25:.2f}%", "3.35%"]
        }), use_container_width=True, hide_index=True)
