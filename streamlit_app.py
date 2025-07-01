import streamlit as st
import pandas as pd
from config import PER_CSV

# Impostazioni pagina
st.set_page_config(
    page_title="Turni Condivisi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titolo principale
st.title("📅 Turni Valerio & Sirya ❤️")

# Funzione per caricare e preparare i dati
@st.cache_data
def carica_turni():
    df = pd.read_csv(PER_CSV, parse_dates=["Data"])
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")  # 🔧 Solo data, senza orario
    df["Giorno"] = df["Giorno"].astype(str)
    df["Fascia Libera Sintetica"] = df["Fascia Libera Sintetica"].astype(str)
    return df

df = carica_turni()

# Sidebar - Filtri
ordine = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]
tutti_giorni = sorted(df["Giorno"].unique().tolist(), key=lambda x: ordine.index(x))
tutti_fasce  = df["Fascia Libera Sintetica"].unique().tolist()

sel_days  = st.sidebar.multiselect("📆 Giorno della settimana", tutti_giorni, default=tutti_giorni)
sel_fasce = st.sidebar.multiselect("⏰ Fascia libera sintetica", tutti_fasce, default=tutti_fasce)

df_f = df[df["Giorno"].isin(sel_days) & df["Fascia Libera Sintetica"].isin(sel_fasce)].reset_index(drop=True)

# Sidebar - Grafico
st.sidebar.subheader("📊 Conteggio fasce sintetiche")
st.sidebar.bar_chart(df_f["Fascia Libera Sintetica"].value_counts())

# Tabella principale
st.markdown("---")
st.dataframe(df_f, use_container_width=True)

# Bottone download CSV
st.download_button(
    label="📥 Scarica dati filtrati (CSV)",
    data=df_f.to_csv(index=False).encode("utf-8"),
    file_name="turni_filtrati.csv",
    mime="text/csv"
)

# Legenda finale
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