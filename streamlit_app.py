import streamlit as st
import pandas as pd
from config import PER_CSV

# Inject CSS per layout responsive e colori più leggibili
def inject_css():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f8;
            color: #2c3e50;
        }

        .title-center {
            text-align: center;
            font-size: 2.3em;
            font-weight: 700;
            margin-top: 20px;
            color: #1a1a1a;
        }

        .legend-box {
            background: #ffffffcc;
            padding: 1.2em;
            border-left: 5px solid #f39c12;
            border-radius: 8px;
            margin-top: 30px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .pdf-button {
            background-color: #2ecc71;
            color: white;
            padding: 0.6em 1.2em;
            border-radius: 6px;
            text-decoration: none;
            font-size: 16px;
        }

        @media screen and (max-width: 768px) {
            .title-center {
                font-size: 1.8em;
            }

            .legend-box {
                font-size: 0.95em;
            }

            table {
                font-size: 14px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Config pagina
st.set_page_config(
    page_title="Turni Condivisi",
    layout="wide"
)

inject_css()

# Titolo principale
st.markdown('<div class="title-center">📅 Turni Valerio & Sirya ❤️</div>', unsafe_allow_html=True)

# Caricamento dati
@st.cache_data
def carica_turni():
    df = pd.read_csv(PER_CSV, parse_dates=["Data"])
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
    df["Giorno"] = df["Giorno"].astype(str)
    df["Fascia Libera Sintetica"] = df["Fascia Libera Sintetica"].astype(str)
    return df

df = carica_turni()

# Tabella principale
st.dataframe(df, use_container_width=True)

# Esportazione dati
st.download_button(
    label="📥 Scarica dati (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="turni_valerio_sirya.csv",
    mime="text/csv"
)

# Se vuoi anche una stampa PDF visiva:
html_export = df.to_html(index=False)
st.markdown("Puoi convertire questo contenuto in PDF tramite 'Stampa → Salva come PDF' dal browser.")

# Legenda
st.markdown('<div class="legend-box">', unsafe_allow_html=True)
st.markdown("**Legenda Fascia Libera Sintetica:**")
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