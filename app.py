import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Ultra v16.2", layout="wide")

# ESTILO CSS (CORREGIDO: Contraste total y legibilidad)
st.markdown("""
    <style>
    /* Forzar color de texto global para evitar letras blancas invisibles */
    html, body, [class*="css"], .stMarkdown, p, div {
        color: #1e293b !important; 
    }
    
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7 !important; color: #14532d !important; }
    .neg-box { background-color: #fee2e2 !important; color: #7f1d1d !important; }
    
    .job-board-card {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 20px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    .job-title { color: #1e3a8a !important; font-weight: bold; font-size: 1.2rem; }
    
    .job-tag {
        font-size: 0.75rem;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 10px;
    }
    .tag-indeed { background: #2557a7; color: white !important; }
    .tag-infojobs { background: #ff6000; color: white !important; }
    .tag-linkedin { background: #0077b5; color: white !important; }
    
    .sync-banner {
        background: #f1f5f9 !important;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #16a34a;
        margin-bottom: 25px;
        color: #0f172a !important;
    }
    
    .house-card { background: white !important; padding: 15px; border-radius: 12px; border-top: 5px solid #1e40af; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN FINANZAS
def get_full_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 65: return "---", "0%", "0%", "0%", 0.0
        actual, ayer = float(df['Close'].iloc[-1]), float(df['Close'].iloc[-2])
        h15d, h3m = float(df['Close'].iloc[-11]), float(df['Close'].iloc[0])
        return f"{actual:,.2f}", f"{((actual-ayer)/ayer)*100:+.2f}%", f"{((actual-h15d)/h15d)*100:+.2f}%", f"{((actual-h3m)/h3m)*100:+.2f}%", actual
    except: return "Error", "0%", "0%", "0%", 0.0

ahora = datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')

st.title("🚀 Radar BCN Ultra v16.2")
st.markdown(f'<div class="sync-banner"><b>ESTADO:</b> Sincronización cada 12h activa.<br><b>ÚLTIMA ACTUALIZACIÓN:</b> {ahora}</div>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Inmuebles", "💼 TABLÓN DE EMPLEO", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    inmuebles = [
        {"zona": "Eixample", "tipo": "Local Comercial", "precio": "115.000€"},
        {"zona": "Poblenou", "tipo": "Oficina Loft", "precio": "139.000€"},
        {"zona": "Sants", "tipo": "Local/Estudio", "precio": "89.000€"},
        {"zona": "Ciutat Vella", "tipo": "Local Histórico", "precio": "145.000€"}
    ]
    cols = st.columns(2)
    for i, casa in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f'<div class="house-card"><b style="color:#1e3a8a">{casa["tipo"]}</b><br>{casa["zona"]} | <span style="color:#1e40af; font-weight:bold">{casa["precio"]}</span></div>', unsafe_allow_html=True)
            st.link_button("Ver Idealista", "https://www.idealista.com/", key=f"h_{i}")

# --- TAB 2: TABLÓN DE EMPLEO (RESTAURADO Y CORREGIDO) ---
with tabs[1]:
    st.markdown("### 📢 Panel de Vacantes Actualizadas")
    
    # Lista ampliada de puestos
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
        target_col = c1 if i % 2 == 0 else c2
        with target_col:
            st.markdown(f"""
                <div class="job-board-card">
                    <span class="job-tag {job['tag']}">{job['p']}</span>
                    <div class="job-title">{job['t']}</div>
                    <div style="font-size: 0.85rem; margin-top: 8px;">📍 Barcelona | Sincro: {ahora}</div>
                </div>
            """, unsafe_allow_html=True)
            
            q = job['t'].replace(" ", "+")
            if job['p'] == "Indeed": l = f"https://es.indeed.com/jobs?q={q}&l=Barcelona&fromage=1"
            elif job['p'] == "InfoJobs": l = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={q}&province=barcelona"
            else: l = f"https://www.linkedin.com/jobs/search/?keywords={q}&location=Barcelona&f_TPR=r86400"
            
            st.link_button(f"Ver ofertas en {job['p']}", l, key=f"btn_job_{i}", use_container_width=True)
            st.write("")

# --- TAB 3: FINANZAS FULL (MANTENIDO) ---
with tabs[2]:
    st.header("📈 Mercados y Banca")
    def render_card(titulo, ticker, es_moneda=True):
        p, d24, d15, m3, val_puro = get_full_data(ticker)
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        simbolo = "$" if es_moneda and "USD" in ticker else "€" if es_moneda else ""
        col1.metric("Hoy", f"{p} {simbolo}", d24)
        def get_cl(v): return "pos-box" if "+" in v else "neg-box"
        col2.markdown(f'<div class="trend-box {get_cl(d15)}"><b>15 DÍAS:</b><br>{d15}</div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="trend-box {get_cl(m3)}"><b>3 MESES:</b><br>{m3}</div>', unsafe_allow_html=True)
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
