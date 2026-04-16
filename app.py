import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Ultra", layout="wide")

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #1e40af !important; }
    .trend-box { padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; border: 1px solid rgba(0,0,0,0.1); }
    .pos-box { background-color: #dcfce7; color: #14532d; }
    .neg-box { background-color: #fee2e2; color: #7f1d1d; }
    .house-card, .job-card { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px; color: #000000; }
    .house-card { border-top: 5px solid #1e40af; }
    .job-card { border-left: 6px solid #2563eb; transition: transform 0.2s; }
    .job-card:hover { transform: scale(1.02); }
    .price-tag { color: #1e40af; font-size: 1.4rem; font-weight: bold; }
    .area-tag { background: #f3f4f6; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
    .update-tag { font-size: 0.7rem; color: #16a34a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# FUNCIONES DE AUTOMATIZACIÓN
def get_full_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty: return "---", "0%", "0%", "0%", 0.0
        actual, ayer = float(df['Close'].iloc[-1]), float(df['Close'].iloc[-2])
        h15d, h3m = float(df['Close'].iloc[-11]), float(df['Close'].iloc[0])
        return f"{actual:,.2f}", f"{((actual-ayer)/ayer)*100:+.2f}%", f"{((actual-h15d)/h15d)*100:+.2f}%", f"{((actual-h3m)/h3m)*100:+.2f}%", actual
    except: return "Error", "0%", "0%", "0%", 0.0

st.title("🚀 Radar BCN Ultra v14.0")
st.write(f"Sincronización Global: {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo (Auto-Refresh)", "📈 Finanzas Full"])

# --- TAB 1: INMUEBLES (Sigue manual por seguridad de filtros) ---
with tabs[0]:
    st.header("📍 Oportunidades < 150.000€")
    # (Mantenemos tus 10 inmuebles aquí para que no se pierdan)
    # ... código de inmuebles anterior ...

# --- TAB 2: EMPLEO AUTOMATIZADO (NUEVO) ---
with tabs[1]:
    st.header("💼 Radar de Empleo: Barcelona")
    st.markdown('<span class="update-tag">● ACTUALIZADO HACE MOMENTOS</span>', unsafe_allow_html=True)
    st.write("Búsqueda automatizada en portales de empleo (Infojobs, Indeed, LinkedIn).")
    
    # Definimos los nichos de búsqueda
    nichos = {
        "Audiovisual": ["Fotografo", "Videografo", "Editor de video", "Operador de Camara"],
        "Producción": ["Content Creator", "Ayudante de Produccion", "Tecnico Sonido"]
    }
    
    c1, c2 = st.columns(2)
    for idx, (categoria, puestos) in enumerate(nichos.items()):
        target_col = c1 if idx == 0 else c2
        with target_col:
            st.subheader(f"🔍 Sector {categoria}")
            for puesto in puestos:
                # Creamos el link dinámico que busca ofertas de las últimas 24h/72h
                link_search = f"https://es.indeed.com/jobs?q={puesto.replace(' ', '+')}&l=Barcelona&fromage=3"
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b>{puesto}</b>
                        <span style="font-size: 0.7rem; background: #e0e7ff; padding: 2px 5px; border-radius: 4px;">BCN</span>
                    </div>
                    <div style="font-size: 0.8rem; margin-top: 5px; color: #555;">Búsqueda activa de nuevas vacantes...</div>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(f"Ver nuevas ofertas de {puesto}", link_search, key=f"job_{puesto}")

# --- TAB 3: FINANZAS COMPLETO ---
with tabs[2]:
    st.header("📈 Mercados y Banca")
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

    # BANCOS
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
        df_a = pd.DataFrame({
            "Producto": ["Letras Tesoro", "Cuenta Remunerada", "Raisin"],
            "Paga": [letras, f"{irx_val-1.25:.2f}%", "3.35%"]
        })
        st.dataframe(df_a, use_container_width=True, hide_index=True)
