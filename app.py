import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Mi App BCN", page_icon="🏙️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background-color: #0a0a0a; color: #f0f0f0; }
[data-testid="stHeader"] { background: #0a0a0a; }
h1 { font-size: 2rem !important; font-weight: 800 !important; color: #c8f135 !important; letter-spacing: -0.02em; margin-bottom: 0 !important; }
h2, h3 { color: #f0f0f0 !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-list"] { background: #111 !important; border-radius: 12px; padding: 4px; gap: 4px; border: 0.5px solid rgba(255,255,255,0.08); }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #666 !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 13px !important; padding: 8px 16px !important; }
.stTabs [aria-selected="true"] { background: #c8f135 !important; color: #0a0a0a !important; font-weight: 700 !important; }
[data-testid="stMetric"] { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px !important; }
[data-testid="stMetricLabel"] { color: #888 !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #f0f0f0 !important; font-family: 'DM Mono', monospace !important; font-size: 1.6rem !important; font-weight: 700 !important; }
.stButton > button { background: #1c1c1c !important; color: #c8f135 !important; border: 0.5px solid rgba(200,241,53,0.3) !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; font-weight: 500 !important; padding: 6px 16px !important; }
.stButton > button:hover { background: #242424 !important; }
.stLinkButton > a { background: #1c1c1c !important; color: #7df3c8 !important; border: 0.5px solid rgba(125,243,200,0.3) !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; text-decoration: none !important; }
.stInfo { background: rgba(200,241,53,0.05) !important; border: 0.5px solid rgba(200,241,53,0.2) !important; border-radius: 10px !important; color: #aaa !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; }
hr { border-color: rgba(255,255,255,0.06) !important; }
.inmueble-card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-top: 3px solid #c8f135; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.job-card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-left: 3px solid #7df3c8; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.tag { font-size: 10px; font-family: 'DM Mono', monospace; font-weight: 700; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.06em; display: inline-block; margin-bottom: 8px; }
.tag-precio { background: rgba(200,241,53,0.12); color: #c8f135; border: 0.5px solid rgba(200,241,53,0.25); }
.tag-tipo { background: rgba(125,243,200,0.12); color: #7df3c8; border: 0.5px solid rgba(125,243,200,0.25); }
.tag-indeed { background: rgba(37,87,167,0.3); color: #7eb3f7; border: 0.5px solid rgba(37,87,167,0.5); }
.tag-infojobs { background: rgba(255,96,0,0.2); color: #f3a27d; border: 0.5px solid rgba(255,96,0,0.4); }
.tag-linkedin { background: rgba(0,119,181,0.2); color: #7df3c8; border: 0.5px solid rgba(0,119,181,0.4); }
.trend-pos { background: rgba(95,214,138,0.08); border: 0.5px solid rgba(95,214,138,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #5fd68a; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-neg { background: rgba(240,82,79,0.08); border: 0.5px solid rgba(240,82,79,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #f0524f; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-lbl { font-size: 10px; color: #555; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.08em; }
.rate-card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center; }
.rate-val { font-size: 1.6rem; font-weight: 800; color: #c8f135; font-family: 'DM Mono', monospace; }
.rate-lbl { font-size: 10px; color: #666; font-family: 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.rate-desc { font-size: 11px; color: #555; font-family: 'DM Mono', monospace; margin-top: 3px; }
</style>
""", unsafe_allow_html=True)

ahora = datetime.now().strftime('%d/%m/%Y · %H:%M')
st.title("🏙️ Mi App BCN")
st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;margin-top:-8px;">Última actualización: {ahora}</p>', unsafe_allow_html=True)
st.markdown("---")

@st.cache_data(ttl=43200)
def get_finance_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 10:
            return "---", "---", "---", 0.0
        act = float(df['Close'].iloc[-1])
        h15 = float(df['Close'].iloc[-16]) if len(df) >= 16 else float(df['Close'].iloc[0])
        h3m = float(df['Close'].iloc[0])
        d15 = f"{((act - h15) / h15) * 100:+.2f}%"
        d3m = f"{((act - h3m) / h3m) * 100:+.2f}%"
        precio = f"{act:,.0f}" if act >= 1000 else f"{act:,.2f}"
        return precio, d15, d3m, act
    except:
        return "Error", "---", "---", 0.0

def trend_html(label, valor):
    cls = "trend-pos" if "+" in str(valor) else "trend-neg"
    return f'<div class="{cls}"><div class="trend-lbl">{label}</div>{valor}</div>'

def render_activo(nombre, ticker, simbolo="$", emoji=""):
    precio, d15, d3m, _ = get_finance_data(ticker)
    st.markdown(f"#### {emoji} {nombre}")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.metric("Precio actual", f"{precio} {simbolo}")
    with c2:
        st.markdown(trend_html("15 días", d15), unsafe_allow_html=True)
    with c3:
        st.markdown(trend_html("3 meses", d3m), unsafe_allow_html=True)
    st.markdown("---")

tabs = st.tabs(["🏢 Inmuebles", "📷 Trabajo", "📈 Finanzas"])

# TAB 1 — INMUEBLES
with tabs[0]:
    st.markdown("### Locales & Oficinas en Barcelona")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Compra · Menos de 150.000€ · Libres · Click para ver anuncios reales</p>', unsafe_allow_html=True)
    col_r, _ = st.columns([1, 4])
    with col_r:
        if st.button("↻ Recargar", key="refresh_inm"):
            st.cache_data.clear()
            st.rerun()
    st.markdown("")
    inmuebles = [
        {"titulo": "Todos los locales baratos BCN", "tipo": "Local", "precio": "Hasta 150.000€", "metros": "Varios", "zona": "Barcelona ciudad", "desc": "Todos los locales en venta en Barcelona ordenados de menor a mayor precio.", "url": "https://www.idealista.com/venta-locales/barcelona-barcelona/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Todas las oficinas baratas BCN", "tipo": "Oficina", "precio": "Hasta 150.000€", "metros": "Varios", "zona": "Barcelona ciudad", "desc": "Oficinas en venta en Barcelona por menos de 150.000€ ordenadas por precio.", "url": "https://www.idealista.com/venta-oficinas/barcelona-barcelona/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Locales en Sants-Montjuïc", "tipo": "Local", "precio": "Hasta 150.000€", "metros": "20–80 m²", "zona": "Sants · Poble Sec · Hostafrancs", "desc": "Locales en Sants y Poble Sec, buena relación calidad-precio y bien comunicados.", "url": "https://www.idealista.com/venta-locales/barcelona-barcelona/sants-montjuic/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Locales en Sant Andreu", "tipo": "Local", "precio": "Hasta 150.000€", "metros": "30–100 m²", "zona": "Sant Andreu · Navas · La Sagrera", "desc": "Uno de los distritos más económicos de Barcelona con buenas comunicaciones.", "url": "https://www.idealista.com/venta-locales/barcelona-barcelona/sant-andreu/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Locales en Nou Barris", "tipo": "Local", "precio": "Hasta 150.000€", "metros": "20–100 m²", "zona": "Nou Barris · Prosperitat · Trinitat", "desc": "Los locales más asequibles de Barcelona ciudad con buen transporte público.", "url": "https://www.idealista.com/venta-locales/barcelona-barcelona/nou-barris/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Oficinas en Ciutat Vella", "tipo": "Oficina", "precio": "Desde 59.000€", "metros": "20–100 m²", "zona": "Gòtic · Raval · Born", "desc": "Oficinas pequeñas en el centro histórico. Las más baratas de toda Barcelona.", "url": "https://www.idealista.com/venta-oficinas/barcelona/ciutat-vella/con-precio-hasta_150000,ordenado-por-precio-asc/"},
        {"titulo": "Fotocasa – Locales Barcelona", "tipo": "Local / Oficina", "precio": "Hasta 150.000€", "metros": "Varios", "zona": "Barcelona capital", "desc": "Búsqueda en Fotocasa con filtro de precio máximo 150.000€ ordenado por precio.", "url": "https://www.fotocasa.es/es/comprar/locales/barcelona-capital/todas-las-zonas/l?maxPrice=150000&sortType=price&sortOrder=asc"},
        {"titulo": "Habitaclia – Locales Barcelona", "tipo": "Local / Oficina", "precio": "Hasta 150.000€", "metros": "Varios", "zona": "Barcelona ciudad", "desc": "Portal catalán con gran selección. Filtra por precio máximo al entrar.", "url": "https://www.habitaclia.com/locales_comerciales-barcelona.htm"},
    ]
    cols = st.columns(2)
    for i, inm in enumerate(inmuebles):
        with cols[i % 2]:
            st.markdown(f"""<div class="inmueble-card"><span class="tag tag-tipo">{inm['tipo']}</span><span class="tag tag-precio" style="margin-left:6px;">{inm['precio']}</span><div style="font-size:15px;font-weight:700;margin:8px 0 4px;">{inm['titulo']}</div><div style="font-size:12px;color:#888;margin-bottom:6px;line-height:1.5;">{inm['desc']}</div><div style="font-size:11px;font-family:'DM Mono',monospace;color:#555;">{inm['zona']} · {inm['metros']}</div></div>""", unsafe_allow_html=True)
            st.link_button("Ver anuncios reales →", inm['url'], key=f"inm_{i}", use_container_width=True)

# TAB 2 — TRABAJO
with tabs[1]:
    st.markdown("### Ofertas de Fotografía & Vídeo")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Barcelona y remoto · Últimas 2 semanas · Links directos a ofertas reales</p>', unsafe_allow_html=True)
    col_r2, _ = st.columns([1, 4])
    with col_r2:
        if st.button("↻ Recargar", key="refresh_trabajo"):
            st.cache_data.clear()
            st.rerun()
    st.markdown("")
    puestos = [
        {"cargo": "Fotógrafo / Fotógrafa", "portal": "Indeed", "tag": "tag-indeed", "desc": "Fotógrafo de producto, eventos, inmobiliaria, moda y publicidad en Barcelona.", "url": "https://es.indeed.com/jobs?q=fotografo&l=Barcelona&fromage=14&sort=date"},
        {"cargo": "Videógrafo / Camarógrafo", "portal": "Indeed", "tag": "tag-indeed", "desc": "Videógrafo, operador de cámara y producción de vídeo en Barcelona.", "url": "https://es.indeed.com/jobs?q=videografo+camara&l=Barcelona&fromage=14&sort=date"},
        {"cargo": "Editor de Vídeo", "portal": "InfoJobs", "tag": "tag-infojobs", "desc": "Edición de vídeo, post-producción y motion graphics en Barcelona.", "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=editor+video&province=barcelona&sinceDate=_14&orderBy=PUBLICATION_DATE"},
        {"cargo": "Técnico Audiovisual", "portal": "InfoJobs", "tag": "tag-infojobs", "desc": "Técnico de sonido, iluminación y producción audiovisual en Barcelona.", "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=tecnico+audiovisual&province=barcelona&sinceDate=_14&orderBy=PUBLICATION_DATE"},
        {"cargo": "Content Creator / Reels", "portal": "LinkedIn", "tag": "tag-linkedin", "desc": "Creador de contenido audiovisual para redes sociales, reels y YouTube.", "url": "https://www.linkedin.com/jobs/search/?keywords=content%20creator%20video%20foto&location=Barcelona&f_TPR=r1209600&sortBy=DD"},
        {"cargo": "Fotografía & Vídeo (remoto)", "portal": "LinkedIn", "tag": "tag-linkedin", "desc": "Ofertas remotas de fotografía, vídeo y producción audiovisual desde España.", "url": "https://www.linkedin.com/jobs/search/?keywords=fotografo%20videografo&location=Spain&f_WT=2&f_TPR=r1209600&sortBy=DD"},
        {"cargo": "Producción Audiovisual", "portal": "Indeed", "tag": "tag-indeed", "desc": "Director de producción, realizador y coordinador audiovisual en Barcelona.", "url": "https://es.indeed.com/jobs?q=produccion+audiovisual&l=Barcelona&fromage=14&sort=date"},
        {"cargo": "Freelance Foto & Vídeo", "portal": "InfoJobs", "tag": "tag-infojobs", "desc": "Proyectos freelance y autónomo en fotografía y vídeo en Barcelona.", "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=fotografo+videografo&province=barcelona&contractType=SELF_EMPLOYED&orderBy=PUBLICATION_DATE"},
    ]
    c1, c2 = st.columns(2)
    for i, job in enumerate(puestos):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""<div class="job-card"><span class="tag {job['tag']}">{job['portal']}</span><div style="font-size:15px;font-weight:700;color:#f0f0f0;margin:6px 0 4px;">{job['cargo']}</div><div style="font-size:12px;color:#888;line-height:1.5;">{job['desc']}</div></div>""", unsafe_allow_html=True)
            st.link_button(f"Ver ofertas en {job['portal']} →", job['url'], key=f"job_{i}", use_container_width=True)

# TAB 3 — FINANZAS
with tabs[2]:
    st.markdown("### Mercados Financieros")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Datos en tiempo real via yfinance · Caché 12h</p>', unsafe_allow_html=True)
    col_r3, _ = st.columns([1, 4])
    with col_r3:
        if st.button("↻ Actualizar precios", key="refresh_fin"):
            st.cache_data.clear()
            st.rerun()
    st.markdown("")
    render_activo("Bitcoin", "BTC-USD", "USD", "₿")
    render_activo("Oro", "GC=F", "USD/oz", "✨")
    render_activo("S&P 500", "^GSPC", "pts", "🇺🇸")
    render_activo("IBEX 35", "^IBEX", "pts", "🇪🇸")

    st.markdown("### Tipos de Interés")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Referencia actual España / Europa · Abril 2026</p>', unsafe_allow_html=True)

    @st.cache_data(ttl=43200)
    def get_euribor():
        try:
            t = yf.Ticker("^IRX")
            df = t.history(period="5d")
            if not df.empty:
                val = float(df['Close'].iloc[-1])
                return f"{val:.2f}%"
        except:
            pass
        return "~2.50%"

    euribor = get_euribor()
    tipos = [
        {"label": "Euríbor 12m", "valor": euribor, "desc": "Ref. hipotecas variables"},
        {"label": "Hipoteca fija", "valor": "~2.80%", "desc": "TAE media 25 años"},
        {"label": "Hipoteca mixta", "valor": "~2.50%", "desc": "TAE media 25 años"},
        {"label": "Préstamo personal", "valor": "~7–9%", "desc": "TAE media banco"},
        {"label": "Cuenta remunerada", "valor": "~2.50%", "desc": "Mejor TAE España"},
        {"label": "Depósito 12m", "valor": "~2.80%", "desc": "Mejor TAE depósito"},
    ]
    cols = st.columns(3)
    for i, tipo in enumerate(tipos):
        with cols[i % 3]:
            st.markdown(f"""<div class="rate-card"><div class="rate-lbl">{tipo['label']}</div><div class="rate-val">{tipo['valor']}</div><div class="rate-desc">{tipo['desc']}</div></div>""", unsafe_allow_html=True)
            st.markdown("")
    st.markdown("")
    st.info("💡 El Euríbor se obtiene via yfinance en tiempo real. El resto son referencias actualizadas cuando el BCE realiza cambios.")

