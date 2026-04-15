import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Radar BCN Premium", layout="wide")

# ESTILO CSS AVANZADO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedor de métricas */
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Precios grandes */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #111827 !important;
    }
    
    /* Tarjetas de Trabajo */
    .job-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .job-card:hover { transform: translateY(-3px); }
    .free-card { border-left-color: #10b981; }
    
    /* Colores dinámicos para texto */
    .pos { color: #10b981; font-weight: bold; }
    .neg { color: #ef4444; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Radar BCN Premium")
st.write(f"📅 {datetime.now().strftime('%A, %d de %B %Y | %H:%Mh')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo", "📈 Finanzas"])

# --- TAB 1: IDEALISTA ---
with tabs[0]:
    st.components.v1.iframe("https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc", height=800, scrolling=True)

# --- TAB 2: TRABAJO ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🛠️ Freelance / Autónomo")
        for t, p in [("Fotógrafo Inmobiliario", "60€/s"), ("Editor Reels", "Proyecto"), ("Cámara Eventos", "250€/d"), ("Retocador Freelance", "Factura"), ("Operador Dron", "A conv.")]:
            st.markdown(f'<div class="job-card free-card"><div style="font-size:1.1rem; font-weight:700;">{t}</div><div style="color:#6b7280;">Pago: {p}</div></div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar a {t}", "https://es.indeed.com", key=t)
            
    with c2:
        st.subheader("👔 Contrato Plantilla")
        for t, s in [("Videógrafo Content", "25k-30k"), ("Fotógrafo Producto", "Jornada"), ("Ayudante Cámara", "Convenio"), ("Editor Post-Prod", "24k"), ("Técnico AV", "22k")]:
            st.markdown(f'<div class="job-card"><div style="font-size:1.1rem; font-weight:700;">{t}</div><div style="color:#6b7280;">Sueldo: {s}</div></div>', unsafe_allow_html=True)
            st.link_button(f"Aplicar a {t}", "https://www.infojobs.net", key=t+"_c")

# --- TAB 3: FINANZAS ESTÉTICAS ---
with tabs[2]:
    st.header("Análisis de Mercado")

    def card_financiera(titulo, precio, d24, d15, m3):
        with st.container():
            st.markdown(f"### {titulo}")
            col1, col2, col3 = st.columns(3)
            
            # 24 Horas (Usando el sistema nativo para la flecha grande)
            col1.metric("Precio / 24h", precio, d24)
            
            # Función para color manual de 15d y 3m
            def color_val(val):
                return "pos" if "+" in val else "neg"
            
            col2.markdown(f"<div class='metric-container'>15 DÍAS<br><span class='{color_val(d15)}' style='font-size:1.5rem;'>{d15}</span></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='metric-container'>3 MESES<br><span class='{color_val(m3)}' style='font-size:1.5rem;'>{m3}</span></div>", unsafe_allow_html=True)
            st.divider()

    card_financiera("₿ Bitcoin (BTC)", "$74,021", "+2.5%", "+12.4%", "+45.0%")
    card_financiera("✨ Oro (XAU)", "2.415,50 €", "-0.8%", "+3.2%", "+8.7%")
    card_financiera("📉 Euríbor 12m", "2,767%", "-0.01%", "-0.12%", "-0.45%")
    card_financiera("🇺🇸 S&P 500", "5.210 pts", "+0.1%", "-1.5%", "+10.2%")

    # Tablas de bancos más limpias
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("### 🏦 Préstamos")
        st.dataframe(pd.DataFrame({"Tipo": ["Fijo", "Variable", "Personal"], "TAE": ["2.20%", "E+0.45%", "6.50%"]}), use_container_width=True)
    with c_b:
        st.markdown("### 💰 Ahorro")
        st.dataframe(pd.DataFrame({"Producto": ["Raisin", "Cuenta Rem.", "Tradic."], "Paga": ["2.85%", "2.10%", "0.75%"]}), use_container_width=True)
