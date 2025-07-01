import pandas as pd
from datetime import datetime

# Percorsi dei file
input_path = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/turni_uniti.csv"
output_path = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/consigli_giornalieri.csv"

print("📂 Leggo il file dei turni uniti...")
df = pd.read_csv(input_path)
df["Data"] = pd.to_datetime(df["Data"])
df["Giorno"] = df["Data"].dt.day_name(locale="it_IT")  # giorno della settimana in italiano

def consiglia(riga):
    fasce = riga["Fascia Libera Comune"]
    giorno = riga["Giorno"]

    if fasce == "Nessuna":
        return "Giornata piena: difficile incastrare qualcosa 😵‍💫"
    
    blocchi = []
    for blocco in fasce.split(";"):
        orari = blocco.strip().split("-")
        if len(orari) != 2:
            continue
        inizio, fine = orari
        try:
            h1 = datetime.strptime(inizio, "%H:%M").time()
            h2 = datetime.strptime(fine, "%H:%M").time()
        except:
            continue

        # Esempi di suggerimenti semplici ma intuitivi
        if h1 >= datetime.strptime("18:00", "%H:%M").time():
            return "Sera libera! Perfetta per una cena fuori o film 🎬"
        elif h1 >= datetime.strptime("14:00", "%H:%M").time() and h2 <= datetime.strptime("18:00", "%H:%M").time():
            return "Pomeriggio libero: palestra? 🏋️‍♂️ o una passeggiata"
        elif h2 <= datetime.strptime("11:30", "%H:%M").time():
            return "Mattina tranquilla: colazione insieme o relax ☕"
        elif h1 <= datetime.strptime("16:00", "%H:%M").time() and h2 >= datetime.strptime("20:00", "%H:%M").time():
            return "Ampio intervallo pomeridiano: organizzate qualcosa insieme 🧡"
    
    return "Fascia libera sparsa: magari una chiamata o un caffè veloce 📱"

print("🧠 Genero consigli giornalieri...")
df["Suggerimento"] = df.apply(consiglia, axis=1)

df[["Data", "Giorno", "Fascia Libera Comune", "Suggerimento"]].to_csv(output_path, index=False, encoding="utf-8")
print(f"✅ File salvato in: {output_path}")