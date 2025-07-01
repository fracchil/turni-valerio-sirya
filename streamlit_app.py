import streamlit as st
import pandas as pd
from config import percorso_csv_uniti

st.set_page_config(
    page_title="Turni Condivisi",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📅 Turni Valerio & Sirya ❤️")

@st.cache_data
def carica_turni():
    df = pd.read_csv(percorso_csv_uniti, parse_dates=["Data"])
    df["Giorno"] = df["Giorno"].astype(str)
    df["Fascia Libera Sintetica"] = df["Fascia Libera Sintetica"].astype(str)
    return df

df = carica_turni()

# Sidebar filtri
ordine = ["Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato","Domenica"]
tutti_giorni = sorted(df["Giorno"].unique().tolist(), key=lambda x: ordine.index(x))
tutti_fasce  = df["Fascia Libera Sintetica"].unique().tolist()

sel_days  = st.sidebar.multiselect("Giorno della settimana", tutti_giorni, default=tutti_giorni)
sel_fasce = st.sidebar.multiselect("Fascia libera sintetica", tutti_fasce, default=tutti_fasce)
df_f = df[df["Giorno"].isin(sel_days) & df["Fascia Libera Sintetica"].isin(sel_fasce)].reset_index(drop=True)

# Styling
def style_sintetica(val):
    cmap = {
        "⚡ Matteriggio libero!":       "#FDEBD0",
        "🔥 Pomesera libero!":          "#F9E79F",
        "🕗 Mattina + 🌇 Sera":          "#D6EAF8",
        "🕗 Mattina":               "#D6EAF8",
        "🌅 Solo pomeriggio":            "#FCF3CF",
        "🌇 Sera":                  "#FDEBD0",
        "🌙 Solo notte disponibile":     "#E8DAEF",
        "🔸 Tempo parziale (<3h utili)": "#F5B7B1",
        "—":                             "#F0F0F0",
        "Non calcolabile":               "#F8D7DA"
    }
    c = cmap.get(val, "#000000")
    return f"color: {c}; font-weight: bold"

st.subheader("📋 Calendario Turni & Fasce Libere")
st.dataframe(
    df_f.style
       .applymap(style_sintetica, subset=["Fascia Libera Sintetica"])
       .set_properties(**{"font-size":"14px","font-family":"sans-serif"}),
    use_container_width=True,
    height=600
)

st.sidebar.subheader("📊 Conteggio fasce sintetiche")
st.sidebar.bar_chart(df_f["Fascia Libera Sintetica"].value_counts())

st.markdown("---")
st.download_button(
    label="📥 Scarica dati filtrati (CSV)",
    data=df_f.to_csv(index=False).encode("utf-8"),
    file_name="turni_filtrati.csv",
    mime="text/csv"
)

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