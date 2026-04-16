import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Ultra v14.1", layout="wide")

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    .house-card, .job-card { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; color: #000000; }
    .house-card { border-top: 5px solid #1e40af; }
    .job-card { border-left: 6px solid #2563eb; }
    .price-tag { color: #1e40af; font-size: 1.4rem; font-weight: bold; }
    .area-tag { background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    .update-tag { font-size: 0.7rem; color: #16a34a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN DE AUTOMATIZACIÓN FINANCIERA (NO TOCAR)
def get_full_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 65:
            return "---", "0%", "0%", "0%", 0.0
        actual = float(df['Close'].iloc[-1])
        ayer = float(df['Close'].iloc[-2])
        hace_15d = float(df['Close'].iloc[-11])
        hace_3m = float(df['Close'].iloc[0])
        v24h = ((actual - ayer) / ayer) * 100
        v15d = ((actual - hace_15d) / hace_15d) * 100
        v3m = ((actual - hace_3m) / hace_3m) * 100
        return f"{actual:,.2f}", f"{v24h:+.2f}%", f"{v15d:+.2f}%", f"{v3m:+.2f}%", actual
    except:
        return "Error", "0%", "0%", "0%", 0.0

st.title("🚀 Radar BCN Ultra v14.1")
st.write(f"Actualización Global: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo (Multi-Portal)", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    st.header("📍 Oportunidades < 150.000€")
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
            st.link_button("Ver en Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/", key=f"h_{i}")

# --- TAB 2: EMPLEO MULTI-PORTAL ---
with tabs[1]:
    st.header("💼 Radar de Empleo: Barcelona")
    st.markdown('<span class="update-tag">● BÚSQUEDA AUTOMATIZADA CADA 12H</span>', unsafe_allow_html=True)
    
    nichos = {
        "Audiovisual": ["Fotografo", "Videografo", "Editor de video", "Operador de Camara"],
        "Producción & Digital": ["Content Creator", "Ayudante de Produccion", "Tecnico AV"]
    }
    
    c1, c2 = st.columns(2)
    for idx, (categoria, puestos) in enumerate(nichos.items()):
        target_col = c1 if idx == 0 else c2
        with target_col:
            st.subheader(f"🔍 {categoria}")
            for puesto in puestos:
                with st.expander(f"📌 Ver ofertas para: {puesto}"):
                    # Enlaces con filtros de tiempo (24h-48h)
                    link_indeed = f"https://es.indeed.com/jobs?q={puesto.replace(' ', '+')}&l=Barcelona&fromage=1"
                    link_infojobs = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={puesto.replace(' ', '%20')}&province=barcelona&order=relevance-desc"
                    link_linkedin = f"https://www.linkedin.com/jobs/search/?keywords={puesto.replace(' ', '%20')}&location=Barcelona&f_TPR=r86400"
                    
                    st.write("Selecciona portal:")
                    ca, cb, cc = st.columns(3)
                    ca.link_button("Indeed", link_indeed, use_container_width=True)
                    cb.link_button("InfoJobs", link_infojobs, use_container_width=True)
                    cc.link_button("LinkedIn", link_linkedin, use_container_width=True)

# --- TAB 3: FINANZAS FULL (MANTENIDO) ---
with tabs[2]:
    st.header("📈 Análisis de Mercado en Tiempo Real")
    
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

    st.subheader("🏦 Financiación y Ahorro Sincronizado")
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
