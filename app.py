import streamlit as st
import yfinance as yf
from datetime import datetime, date
import json

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
.stLinkButton > a { background: #1c1c1c !important; color: #7df3c8 !important; border: 0.5px solid rgba(125,243,200,0.3) !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; text-decoration: none !important; }
hr { border-color: rgba(255,255,255,0.06) !important; }
.card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.card-job { border-left: 3px solid #7df3c8; }
.tag { font-size: 10px; font-family: 'DM Mono', monospace; font-weight: 700; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.06em; display: inline-block; margin-bottom: 8px; }
.tag-indeed { background: rgba(37,87,167,0.3); color: #7eb3f7; border: 0.5px solid rgba(37,87,167,0.5); }
.tag-infojobs { background: rgba(255,96,0,0.2); color: #f3a27d; border: 0.5px solid rgba(255,96,0,0.4); }
.tag-linkedin { background: rgba(0,119,181,0.2); color: #7df3c8; border: 0.5px solid rgba(0,119,181,0.4); }
.tag-domestika { background: rgba(220,60,60,0.2); color: #f7857d; border: 0.5px solid rgba(220,60,60,0.4); }
.filtro-box { background: rgba(200,241,53,0.04); border: 0.5px solid rgba(200,241,53,0.15); border-radius: 10px; padding: 12px 16px; margin-bottom: 20px; font-family: 'DM Mono', monospace; font-size: 12px; color: #888; line-height: 1.8; }
.filtro-box strong { color: #c8f135; }
.instruccion { font-size: 11px; font-family: 'DM Mono', monospace; color: #c8f135; background: rgba(200,241,53,0.06); padding: 6px 10px; border-radius: 6px; margin-top: 8px; }
.trend-pos { background: rgba(95,214,138,0.08); border: 0.5px solid rgba(95,214,138,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #5fd68a; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-neg { background: rgba(240,82,79,0.08); border: 0.5px solid rgba(240,82,79,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #f0524f; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-lbl { font-size: 10px; color: #555; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.08em; }
.rate-card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center; margin-bottom: 8px; }
.rate-val { font-size: 1.6rem; font-weight: 800; color: #c8f135; font-family: 'DM Mono', monospace; }
.rate-lbl { font-size: 10px; color: #666; font-family: 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.rate-desc { font-size: 11px; color: #555; font-family: 'DM Mono', monospace; margin-top: 3px; }
.no-datos { background: rgba(255,255,255,0.03); border: 0.5px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 24px; text-align: center; font-family: 'DM Mono', monospace; color: #444; font-size: 13px; }
.no-datos span { font-size: 28px; display: block; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

ahora = datetime.now().strftime('%d/%m/%Y · %H:%M')
st.title("🏙️ Mi App BCN")
st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;margin-top:-8px;">{ahora}</p>', unsafe_allow_html=True)
st.markdown("---")

# ── FINANZAS ──────────────────────────────────────────────────
# Cache hasta fin del día actual
def segundos_hasta_medianoche():
    now = datetime.now()
    midnight = datetime.combine(now.date(), datetime.min.time()).replace(hour=0, minute=0, second=0)
    from datetime import timedelta
    midnight += timedelta(days=1)
    return max(int((midnight - now).total_seconds()), 60)

@st.cache_data(ttl=segundos_hasta_medianoche())
def get_finance_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="6mo")
        if df.empty or len(df) < 10:
            return None
        act = float(df['Close'].iloc[-1])
        h15 = float(df['Close'].iloc[-16]) if len(df) >= 16 else float(df['Close'].iloc[0])
        h3m = float(df['Close'].iloc[0])
        d15 = ((act - h15) / h15) * 100
        d3m = ((act - h3m) / h3m) * 100
        precio = f"{act:,.0f}" if act >= 1000 else f"{act:,.2f}"
        return {"precio": precio, "d15": d15, "d3m": d3m, "act": act, "fecha": str(date.today())}
    except:
        return None

def trend_html(label, valor):
    signo = "+" if valor >= 0 else ""
    cls = "trend-pos" if valor >= 0 else "trend-neg"
    return f'<div class="{cls}"><div class="trend-lbl">{label}</div>{signo}{valor:.2f}%</div>'

def render_activo(nombre, ticker, simbolo, emoji):
    data = get_finance_data(ticker)
    st.markdown(f"#### {emoji} {nombre}")
    if data is None:
        st.markdown('<div class="no-datos"><span>📡</span>Sin datos hoy — mercado cerrado o sin conexión</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.metric("Precio actual", f"{data['precio']} {simbolo}")
        with c2:
            st.markdown(trend_html("15 días", data['d15']), unsafe_allow_html=True)
        with c3:
            st.markdown(trend_html("3 meses", data['d3m']), unsafe_allow_html=True)
    st.markdown("---")

@st.cache_data(ttl=segundos_hasta_medianoche())
def get_euribor():
    try:
        t = yf.Ticker("^IRX")
        df = t.history(period="5d")
        if not df.empty:
            return f"{float(df['Close'].iloc[-1]):.2f}%"
    except:
        pass
    return None

# ── TABS ──────────────────────────────────────────────────────
tabs = st.tabs(["📷 Trabajo", "📈 Finanzas"])

# ══ TAB 1 — TRABAJO ════════════════════════════════════════════
with tabs[0]:
    st.markdown("### Ofertas de Fotografía & Vídeo")
    st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Barcelona y remoto · Actualizado: {ahora}</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="filtro-box">
        🔍 Al entrar en cada portal aplica estos filtros:<br>
        <strong>Fecha:</strong> Última semana o últimos 14 días &nbsp;·&nbsp;
        <strong>Zona:</strong> Barcelona / Remoto &nbsp;·&nbsp;
        <strong>Tipo:</strong> Todos los contratos
    </div>
    """, unsafe_allow_html=True)

    puestos = [
        {
            "cargo": "Fotógrafo / Fotógrafa",
            "portal": "Indeed", "tag": "tag-indeed",
            "desc": "Fotografía de producto, eventos, inmobiliaria, moda y publicidad en Barcelona.",
            "filtro": "Busca: 'fotografo' · Zona: Barcelona · Fecha: 14 días",
            "url": "https://es.indeed.com/jobs?q=fotografo&l=Barcelona&fromage=14&sort=date"
        },
        {
            "cargo": "Videógrafo / Camarógrafo",
            "portal": "Indeed", "tag": "tag-indeed",
            "desc": "Videógrafo, operador de cámara y producción de vídeo en Barcelona.",
            "filtro": "Busca: 'videografo' · Zona: Barcelona · Fecha: 14 días",
            "url": "https://es.indeed.com/jobs?q=videografo&l=Barcelona&fromage=14&sort=date"
        },
        {
            "cargo": "Editor de Vídeo / Post-producción",
            "portal": "InfoJobs", "tag": "tag-infojobs",
            "desc": "Edición de vídeo, post-producción, color grading y motion graphics.",
            "filtro": "Busca: 'editor video' · Provincia: Barcelona · Fecha: 14 días",
            "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=editor+video&province=barcelona&sinceDate=_14"
        },
        {
            "cargo": "Técnico Audiovisual",
            "portal": "InfoJobs", "tag": "tag-infojobs",
            "desc": "Técnico de sonido, iluminación y producción audiovisual en Barcelona.",
            "filtro": "Busca: 'tecnico audiovisual' · Provincia: Barcelona · Fecha: 14 días",
            "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=tecnico+audiovisual&province=barcelona&sinceDate=_14"
        },
        {
            "cargo": "Content Creator / Reels",
            "portal": "LinkedIn", "tag": "tag-linkedin",
            "desc": "Creador de contenido audiovisual para redes sociales, reels y YouTube.",
            "filtro": "Busca: 'content creator video' · Zona: Barcelona · Fecha: 2 semanas",
            "url": "https://www.linkedin.com/jobs/search/?keywords=content+creator+video&location=Barcelona&f_TPR=r1209600"
        },
        {
            "cargo": "Fotografía & Vídeo (remoto)",
            "portal": "LinkedIn", "tag": "tag-linkedin",
            "desc": "Ofertas 100% remotas de fotografía y vídeo desde cualquier parte de España.",
            "filtro": "Busca: 'fotografo videografo' · Remoto · España · Fecha: 2 semanas",
            "url": "https://www.linkedin.com/jobs/search/?keywords=fotografo+videografo&location=Spain&f_WT=2&f_TPR=r1209600"
        },
        {
            "cargo": "Producción Audiovisual",
            "portal": "Indeed", "tag": "tag-indeed",
            "desc": "Director, realizador y coordinador de producción audiovisual en Barcelona.",
            "filtro": "Busca: 'produccion audiovisual' · Zona: Barcelona · Fecha: 14 días",
            "url": "https://es.indeed.com/jobs?q=produccion+audiovisual&l=Barcelona&fromage=14&sort=date"
        },
        {
            "cargo": "Cursos & Freelance Foto/Vídeo",
            "portal": "Domestika", "tag": "tag-domestika",
            "desc": "Proyectos creativos, colaboraciones y oportunidades freelance en fotografía y vídeo.",
            "filtro": "Explora trabajos creativos y proyectos freelance en tu área",
            "url": "https://www.domestika.org/es/jobs?q=fotografia+video"
        },
        {
            "cargo": "Freelance Foto & Vídeo",
            "portal": "InfoJobs", "tag": "tag-infojobs",
            "desc": "Proyectos freelance y autónomo en fotografía y vídeo en Barcelona.",
            "filtro": "Busca: 'fotografo videografo' · Autónomo · Barcelona",
            "url": "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=fotografo+videografo&province=barcelona&contractType=SELF_EMPLOYED"
        },
        {
            "cargo": "Operador de Cámara / Drone",
            "portal": "LinkedIn", "tag": "tag-linkedin",
            "desc": "Operador de cámara, piloto de drone y toma aérea en Barcelona y alrededores.",
            "filtro": "Busca: 'operador camara drone' · Barcelona · Fecha: 2 semanas",
            "url": "https://www.linkedin.com/jobs/search/?keywords=operador+camara+drone&location=Barcelona&f_TPR=r1209600"
        },
    ]

    cols = st.columns(2)
    for i, job in enumerate(puestos):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card card-job">
                <span class="tag {job['tag']}">{job['portal']}</span>
                <div style="font-size:15px;font-weight:700;color:#f0f0f0;margin:6px 0 4px;">{job['cargo']}</div>
                <div style="font-size:12px;color:#888;line-height:1.5;margin-bottom:6px;">{job['desc']}</div>
                <div class="instruccion">📌 {job['filtro']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"Ver en {job['portal']} →", job['url'], key=f"job_{i}", use_container_width=True)

# ══ TAB 2 — FINANZAS ═══════════════════════════════════════════
with tabs[1]:
    st.markdown("### Mercados Financieros")

    hoy = date.today().strftime('%d/%m/%Y')
    # Comprobar si hay datos de hoy
    data_btc = get_finance_data("BTC-USD")
    if data_btc and data_btc.get("fecha") == str(date.today()):
        st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Datos de hoy · {hoy} · Se actualizan automáticamente cada día</p>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="no-datos" style="margin-bottom:20px;">
            <span>📭</span>
            <strong style="color:#888;">Sin reposición hoy ({hoy})</strong><br>
            <span style="font-size:12px;">Puede que los mercados estén cerrados o sin datos disponibles todavía</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    render_activo("Bitcoin", "BTC-USD", "USD", "₿")
    render_activo("Oro", "GC=F", "USD/oz", "✨")
    render_activo("S&P 500", "^GSPC", "pts", "🇺🇸")
    render_activo("IBEX 35", "^IBEX", "pts", "🇪🇸")

    st.markdown("### Tipos de Interés")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">España / Europa · Referencia Abril 2026</p>', unsafe_allow_html=True)

    euribor = get_euribor()
    tipos = [
        {"label": "Euríbor 12m", "valor": euribor if euribor else "N/D", "desc": "Ref. hipotecas variables"},
        {"label": "Hipoteca fija", "valor": "~2.80%", "desc": "TAE media 25 años"},
        {"label": "Hipoteca mixta", "valor": "~2.50%", "desc": "TAE media 25 años"},
        {"label": "Préstamo personal", "valor": "~7–9%", "desc": "TAE media banco"},
        {"label": "Cuenta remunerada", "valor": "~2.50%", "desc": "Mejor TAE España"},
        {"label": "Depósito 12m", "valor": "~2.80%", "desc": "Mejor TAE depósito"},
    ]
    cols = st.columns(3)
    for i, tipo in enumerate(tipos):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="rate-card">
                <div class="rate-lbl">{tipo['label']}</div>
                <div class="rate-val">{tipo['valor']}</div>
                <div class="rate-desc">{tipo['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    if euribor is None:
        st.warning("⚠️ No se pudo obtener el Euríbor hoy. Se mostrará cuando los mercados abran.")
    else:
        st.info("💡 El Euríbor se actualiza automáticamente cada día. El resto son referencias que se actualizan cuando el BCE realiza cambios.")

