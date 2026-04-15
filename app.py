import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Pro", layout="wide")

# ESTILO CSS MEJORADO
st.markdown("""
    <style>
    /* PRECIO PRINCIPAL EN COLOR AZUL NAVY */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #1e40af !important; /* Azul intenso profesional */
    }
    
    /* Cajas de Tendencia con Contraste Máximo */
    .trend-box {
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
        border: 1px solid rgba(0,0,0,0.1);
    }
    .pos-box { background-color: #dcfce7; color: #14532d; } /* Verde suave fondo, verde muy oscuro letra */
    .neg-box { background-color: #fee2e2; color: #7f1d1d; } /* Rojo suave fondo, rojo muy oscuro letra */
    
    .trend-label { font-size: 0.8rem; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; color: #4b5563; }
    .trend-value { font-size: 1.4rem; font-weight: 800; }

    /* Tarjetas de Trabajo */
    .job-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        color: #000000;
    }
    .free-card { border-left-color: #16a34a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Radar BCN Premium")
st.write(f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo", "📈 Finanzas"])

# --- TAB 1: INMUEBLES ---
with tabs[0]:
    st.components.v1.iframe("https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc", height=700, scrolling=True)

# --- TAB 2: TRABAJO ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛠️ Freelance")
        for t, p in [("Fotógrafo Inmobiliario", "60€/s"), ("Editor Reels", "Proyecto"), ("Cámara Eventos", "250€/d"), ("Retocador Freelance", "Factura"), ("Operador Dron", "A conv.")]:
            st.markdown(f'<div class="job-card free-card"><b>{t}</b><br>Pago: {p}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://es.indeed.com", key=t)
    with c2:
        st.subheader("👔 Contrato")
        for t, s in [("Videógrafo Content", "25k-30k"), ("Fotógrafo Producto", "Jornada"), ("Ayudante Cámara", "Convenio"), ("Editor Post-Prod", "24k"), ("Técnico AV", "22k")]:
            st.markdown(f'<div class="job-card"><b>{t}</b><br>Sueldo: {s}</div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS (PRECIOS EN COLOR) ---
with tabs[2]:
    st.header("Análisis de Mercado")

    def card_financiera(titulo, precio, d24, d15, m3):
        st.markdown(f"### {titulo}")
        col1, col2, col3 = st.columns(3)
        
        # 24 Horas con precio en Azul
        col1.metric("Precio / 24h", precio, d24)
        
        def get_class(val): return "pos-box" if "+" in val else "neg-box"
        
        # Cajas con letras oscuras para que se lean perfecto
        col2.markdown(f"""<div class="trend-box {get_class(d15)}">
            <div class="trend-label">15 Días</div>
            <div class="trend-value">{d15}</div>
        </div>""", unsafe_allow_html=True)
        
        col3.markdown(f"""<div class="trend-box {get_class(m3)}">
            <div class="trend-label">3 Meses</div>
            <div class="trend-value">{m3}</div>
        </div>""", unsafe_allow_html=True)
        st.divider()

    card_financiera("₿ Bitcoin (BTC)", "$74.021", "+2.5%", "+12.4%", "+45.0%")
    card_financiera("✨ Oro (XAU)", "2.415,50 €", "-0.8%", "+3.2%", "+8.7%")
    card_financiera("📉 Euríbor 12m", "2,767%", "-0.01%", "-0.12%", "-0.45%")
    card_financiera("🇺🇸 S&P 500", "5.210 pts", "+0.1%", "-1.5%", "+10.2%")

    st.subheader("🏦 Bancos y Ahorro")
    c_a, c_b = st.columns(2)
    with c_a:
        st.dataframe(pd.DataFrame({"Préstamos": ["Fijo", "Variable", "Personal"], "TAE": ["2.20%", "E+0.45%", "6.50%"]}), use_container_width=True)
    with c_b:
        st.dataframe(pd.DataFrame({"Ahorro": ["Raisin", "Cuenta Rem.", "Tradic."], "Paga": ["2.85%", "2.10%", "0.75%"]}), use_container_width=True)
