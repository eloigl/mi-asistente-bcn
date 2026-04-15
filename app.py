import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Mi Asistente BCN", layout="wide")

# Estilo para que se vea profesional en el móvil
st.markdown("""
    <style>
    .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Mi Panel de Control BCN")
st.write(f"Actualizado hoy: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

tabs = st.tabs(["🏠 Inmuebles", "💼 Empleo Foto/Vídeo", "💰 Finanzas y Bancos"])

# --- TAB 1: INMUEBLES (BÚSQUEDA REAL) ---
with tabs[0]:
    st.header("Locales y Oficinas BCN")
    st.info("Filtros: Barcelona Capital | < 150.000€ | Sin Okupas")
    
    # Generamos links de búsqueda real que se actualizan al clic
    st.write("Haz clic para abrir los resultados reales de este momento:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("🔍 Ver en Idealista", "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000/?orden=publicado-desc")
    with col2:
        st.link_button("🔍 Ver en Habitaclia", "https://www.habitaclia.com/venta-locales_comerciales-barcelona-hasta_150000.htm?ordenar=mas_recientes")
    with col3:
        st.link_button("🔍 Ver en Fotocasa", "https://www.fotocasa.es/es/comprar/locales/barcelona-capital/l?maxPrice=150000&sortOrder=publicationDate")

    st.divider()
    st.subheader("⚠️ Recordatorio Anti-Okupas")
    st.warning("Al entrar en los links, descarta anuncios que digan: 'Inmueble sin posesión', 'Venta de nuda propiedad' o 'No se puede visitar'.")

# --- TAB 2: EMPLEO ---
with tabs[1]:
    st.header("Oportunidades Foto y Vídeo")
    # Buscador directo a las secciones de empleo en BCN
    st.write("Ofertas frescas en Barcelona:")
    st.link_button("🎥 Ver ofertas de Vídeo (LinkedIn)", "https://www.linkedin.com/jobs/search/?keywords=video&location=Barcelona")
    st.link_button("📸 Ver ofertas de Fotografía (Infojobs)", "https://www.infojobs.net/jobsearch/search-v2.xhtml?keywords=fotografo&province=barcelona")

# --- TAB 3: FINANZAS COMPLETAS (ACTUALIZADO 15/04/2026) ---
with tabs[2]:
    st.header("Estado de los Mercados")
    
    # Bloque de Cripto y Bolsa
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Bitcoin (BTC)", "$74.021", "+2.5%")
    with c2:
        st.metric("Oro (oz)", "2.415,50 €", "-0.8%")
    with c3:
        st.metric("S&P 500", "5.210 pts", "+0.1%")

    st.divider()
    
    # Bloque de Bancos y Préstamos
    st.subheader("🏦 Tipos de Interés en España")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### Préstamos e Hipotecas")
        data_prestamos = {
            "Producto": ["Euríbor 12 meses", "Hipotecas Fijas", "Hipotecas Variables", "Préstamo Efectivo"],
            "Tasa Actual": ["2,767%", "2,20% TAE", "Euríbor + 0,45%", "4,50% - 7,50%"]
        }
        st.table(pd.DataFrame(data_prestamos))
        
    with col_b:
        st.write("### Rentabilidad Ahorro")
        data_ahorro = {
            "Banco / Tipo": ["Mejor Depósito (Raisin)", "Banca Tradicional", "Cuentas Remuneradas"],
            "Tasa Actual": ["2,85% TAE", "0,50% - 1,00%", "2,00% TAE"]
        }
        st.table(pd.DataFrame(data_ahorro))

    st.info("💡 Consejo: Los intereses de los depósitos están en su punto más alto del trimestre.")
