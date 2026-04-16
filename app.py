import streamlit as st
import yfinance as yf
from datetime import datetime, date
import json
import os

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
.trend-pos { background: rgba(95,214,138,0.08); border: 0.5px solid rgba(95,214,138,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #5fd68a; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-neg { background: rgba(240,82,79,0.08); border: 0.5px solid rgba(240,82,79,0.2); border-radius: 10px; padding: 12px; text-align: center; color: #f0524f; font-family: 'DM Mono', monospace; font-weight: 700; font-size: 1.1rem; }
.trend-lbl { font-size: 10px; color: #555; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.08em; }
.rate-card { background: #141414; border: 0.5px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center; margin-bottom: 8px; }
.rate-val { font-size: 1.6rem; font-weight: 800; color: #c8f135; font-family: 'DM Mono', monospace; }
.rate-lbl { font-size: 10px; color: #666; font-family: 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.rate-desc { font-size: 11px; color: #555; font-family: 'DM Mono', monospace; margin-top: 3px; }
.no-datos { background: rgba(255,255,255,0.03); border: 0.5px dashed rgba(255,255,255,0.1); border-radius: 12px; padding: 28px; text-align: center; font-family: 'DM Mono', monospace; color: #555; font-size: 13px; line-height: 1.8; }
.no-datos-icon { font-size: 32px; display: block; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

ahora = datetime.now().strftime('%d/%m/%Y · %H:%M')
st.title("🏙️ Mi App BCN")
st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;margin-top:-8px;">{ahora}</p>', unsafe_allow_html=True)
st.markdown("---")

# ── HELPERS FINANZAS ──────────────────────────────────────────
def segundos_hasta_medianoche():
    from datetime import timedelta
    now = datetime.now()
    midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
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
        return {
            "precio": f"{act:,.0f}" if act >= 1000 else f"{act:,.2f}",
            "d15": ((act - h15) / h15) * 100,
            "d3m": ((act - h3m) / h3m) * 100,
        }
    except:
        return None

@st.cache_data(ttl=segundos_hasta_medianoche())
def get_euribor():
    try:
        df = yf.Ticker("^IRX").history(period="5d")
        if not df.empty:
            return f"{float(df['Close'].iloc[-1]):.2f}%"
    except:
        pass
    return None

def trend_html(label, valor):
    signo = "+" if valor >= 0 else ""
    cls = "trend-pos" if valor >= 0 else "trend-neg"
    return f'<div class="{cls}"><div class="trend-lbl">{label}</div>{signo}{valor:.2f}%</div>'

def render_activo(nombre, ticker, simbolo, emoji):
    data = get_finance_data(ticker)
    st.markdown(f"#### {emoji} {nombre}")
    if data is None:
        st.markdown('<div class="no-datos"><span class="no-datos-icon">📡</span>Sin datos hoy — mercado cerrado o sin conexión</div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.metric("Precio actual", f"{data['precio']} {simbolo}")
        with c2:
            st.markdown(trend_html("15 días", data['d15']), unsafe_allow_html=True)
        with c3:
            st.markdown(trend_html("3 meses", data['d3m']), unsafe_allow_html=True)
    st.markdown("---")

# ── CARGAR TRABAJOS ───────────────────────────────────────────
def cargar_trabajos():
    ruta = "data/trabajos.json"
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# ── TABS ──────────────────────────────────────────────────────
tabs = st.tabs(["📷 Trabajo", "📈 Finanzas"])

# ══ TAB 1 — TRABAJO ════════════════════════════════════════════
with tabs[0]:
    st.markdown("### Ofertas de Fotografía & Vídeo")

    datos = cargar_trabajos()
    hoy = str(date.today())

    if datos is None or datos.get("total", 0) == 0:
        # Sin datos todavía o sin ofertas hoy
        fecha_txt = datos.get("actualizado", "") if datos else ""
        st.markdown(f"""
        <div class="no-datos">
            <span class="no-datos-icon">📭</span>
            <strong style="color:#888;">Sin nuevas ofertas hoy</strong><br>
            No se encontraron publicaciones nuevas en los portales.<br>
            El bot vuelve a buscar mañana a las 8:00h.
            {f'<br><span style="color:#444;font-size:11px;">Última búsqueda: {fecha_txt}</span>' if fecha_txt else ''}
        </div>
        """, unsafe_allow_html=True)

    else:
        es_hoy = datos.get("fecha") == hoy
        color_fecha = "#5fd68a" if es_hoy else "#888"
        label_fecha = f"Hoy · {datos.get('actualizado','')}" if es_hoy else f"Última actualización: {datos.get('actualizado','')}"

        st.markdown(f'<p style="font-family:\'DM Mono\',monospace;color:{color_fecha};font-size:12px;">{label_fecha} · {datos.get("total",0)} ofertas encontradas</p>', unsafe_allow_html=True)

        if not es_hoy:
            st.warning("⚠️ Estos datos son de ayer o anteriores. El bot actualizará esta mañana a las 8:00h.")

        st.markdown("")

        ofertas = datos.get("ofertas", [])
        cols = st.columns(2)
        for i, job in enumerate(ofertas):
            tag_cls = "tag-indeed" if job.get("portal") == "Indeed" else "tag-infojobs"
            with cols[i % 2]:
                st.markdown(f"""
                <div class="card card-job">
                    <span class="tag {tag_cls}">{job.get('portal','')}</span>
                    <div style="font-size:15px;font-weight:700;color:#f0f0f0;margin:6px 0 4px;">{job.get('cargo','')}</div>
                    <div style="font-size:13px;font-family:'DM Mono',monospace;color:#7df3c8;margin-bottom:4px;">{job.get('empresa','')}</div>
                    <div style="font-size:12px;color:#666;">{job.get('ubicacion','Barcelona')}</div>
                </div>
                """, unsafe_allow_html=True)
                st.link_button("Ver oferta →", job.get("url", "#"), key=f"job_{i}", use_container_width=True)

# ══ TAB 2 — FINANZAS ═══════════════════════════════════════════
with tabs[1]:
    st.markdown("### Mercados Financieros")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">Se actualizan automáticamente cada día</p>', unsafe_allow_html=True)
    st.markdown("")

    render_activo("Bitcoin", "BTC-USD", "USD", "₿")
    render_activo("Oro", "GC=F", "USD/oz", "✨")
    render_activo("S&P 500", "^GSPC", "pts", "🇺🇸")
    render_activo("IBEX 35", "^IBEX", "pts", "🇪🇸")

    st.markdown("### Tipos de Interés")
    st.markdown('<p style="font-family:\'DM Mono\',monospace;color:#555;font-size:12px;">España / Europa · Referencia Abril 2026</p>', unsafe_allow_html=True)

    euribor = get_euribor()
    tipos = [
        {"label": "Euríbor 12m", "valor": euribor or "N/D", "desc": "Ref. hipotecas variables"},
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


