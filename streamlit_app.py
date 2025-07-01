import streamlit as st
import pandas as pd
from config import PER_CSV

# Inject CSS custom
def inject_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
        }

        .title-center {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333333;
            margin-top: 20px;
        }

        .legend-box {
            background-color: #ffffffee;
            padding: 1em;
            border-left: 6px solid #f39c12;
            border-radius: 8px;
            box-shadow: 1px 1px 8px rgba(0,0,0,0.08);
            margin-top: 20px;
        }

        hr {
            border: none;
            border-top: 1px solid #dddddd;
            margin: 30px 0;
        }
        </style>
    """, unsafe_allow_html=True)

# Impostazioni iniziali
st.set_page_config(
    page_title="Turni Condivisi",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# Titolo principale
st.markdown('<div class="title-center">📅 Turni Valerio & Sirya ❤️</div>', unsafe_allow_html=True)

# Carica i dati
@st.cache_data
def carica_turni():
    df = pd.read_csv(PER_CSV, parse_dates=["Data"])
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")  # ✅ data formattata
    df["Giorno"] = df["Giorno"].astype(str)
    df["Fascia Libera Sintetica"] = df["Fascia Libera Sintetica"].astype(str)
    return df

df = carica_turni()

# Sidebar: filtri
ordine = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]
tutti_giorni = sorted(df["Giorno"].unique().tolist(), key=lambda x: ordine.index(x))
tutti_fasce  = df["Fascia Libera Sintetica"].unique().tolist()

sel_days  = st.sidebar.multiselect("📆 Giorno della settimana", tutti_giorni, default=tutti_giorni)
sel_fasce = st.sidebar.multiselect("⏰ Fascia libera sintetica", tutti_fasce, default=tutti_fasce)

df_f = df[df["Giorno"].isin(sel_days) & df["Fascia Libera Sintetica"].isin(sel_fasce)].reset_index(drop=True)

# Sidebar: grafico
st.sidebar.subheader("📊 Conteggio fasce sintetiche")
st.sidebar.bar_chart(df_f["Fascia Libera Sintetica"].value_counts())

# Tabella
st.markdown("---")
st.dataframe(df_f, use_container_width=True)

# Download CSV
st.download_button(
    label="📥 Scarica dati filtrati (CSV)",
    data=df_f.to_csv(index=False).encode("utf-8"),
    file_name="turni_filtrati.csv",
    mime="text/csv"
)

# Legenda finale
st.markdown('<div class="legend-box">', unsafe_allow_html=True)
st.markdown("**Legenda Fascia Libera Sintetica**")
st.markdown("""
- ⚡ Matteriggio libero!  
- 🔥 Pomesera libero!  
- 🕗 Mattina + 🌇 Sera  
- 🕗 Solo mattina  
- 🌅 Solo pomeriggio  
- 🌇 Solo sera  
- 🌙 Solo notte disponibile  
- 🔸 Tempo parziale (<3h utili)  
- Non calcolabile (turni indefiniti)  
""")
st.markdown('</div>', unsafe_allow_html=True)