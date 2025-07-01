import streamlit as st
import pandas as pd
from config import PER_CSV
from io import StringIO

# ▶️ Configurazione pagina
st.set_page_config(
    page_title="Turni Valerio & Sirya",
    layout="wide"
)

# ▶️ Stile CSS: mobile-friendly + export layout
def css_mobile():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f2f2f2;
            color: #111111;
        }
        .turno-card {
            background: #ffffff;
            border-left: 5px solid #3498db;
            padding: 1em;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }
        .turno-card h4 {
            margin: 0;
            font-size: 1.25em;
            color: #000000;
        }
        .turno-card p {
            margin: 6px 0 0 0;
            font-size: 0.96em;
            color: #333333;
        }
        .legend-box {
            background-color: #ffffffcc;
            padding: 1.2em;
            border-left: 5px solid #e67e22;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            color: #111111;
        }
        @media screen and (max-width: 768px) {
            .turno-card { font-size: 1em; }
            .legend-box { font-size: 0.95em; }
            body { font-size: 16px !important; }
        }
    </style>
    """, unsafe_allow_html=True)

css_mobile()

# ▶️ Titolo
st.markdown("<h1 style='text-align:center;'>📅 Turni Valerio & Sirya ❤️</h1>", unsafe_allow_html=True)

# ▶️ Caricamento dati
@st.cache_data
def carica_turni():
    df = pd.read_csv(PER_CSV, parse_dates=["Data"])
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
    df["Giorno"] = df["Giorno"].astype(str)
    df["Fascia Libera Sintetica"] = df["Fascia Libera Sintetica"].astype(str)
    return df

df = carica_turni()

# ▶️ Esportazione HTML (per PDF)
def export_html(df):
    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Segoe UI, sans-serif; margin: 2em; color: #222; }}
        h2 {{ text-align: center; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            font-size: 14px;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
    </style>
    </head>
    <body>
        <h2>📄 Turni aggiornati — Valerio & Sirya</h2>
        {df.to_html(index=False)}
    </body>
    </html>
    """
    return html.encode("utf-8")

html_bytes = export_html(df)
st.download_button(
    label="📤 Esporta versione PDF-friendly (HTML)",
    data=html_bytes,
    file_name="turni_valerio_sirya.html",
    mime="text/html"
)

# ▶️ Visualizzazione mobile-friendly → CARD PER RIGA
st.subheader("📋 Elenco turni")

for _, row in df.iterrows():
    st.markdown(f"""
    <div class="turno-card">
        <h4>📆 {row["Data"]}</h4>
        <p><strong>🧍 {row.get("Nome", "—")}</strong></p>
        <p>⏰ Fascia: <em>{row["Fascia Libera Sintetica"]}</em></p>
    </div>
    """, unsafe_allow_html=True)

# ▶️ Legenda finale
st.markdown('<div class="legend-box">', unsafe_allow_html=True)
st.markdown("**Legenda Fascia Libera Sintetica**")
st.markdown("""
- ⚡ Matteriggio libero  
- 🔥 Pomesera libero  
- 🕗 Mattina + 🌇 Sera  
- 🕗 Solo mattina  
- 🌅 Solo pomeriggio  
- 🌇 Solo sera  
- 🌙 Solo notte disponibile  
- 🔸 Tempo parziale (<3h utili)  
- Non calcolabile (turni indefiniti)  
""")
st.markdown('</div>', unsafe_allow_html=True)