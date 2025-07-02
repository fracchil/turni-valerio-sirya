from config import UTENTI
from moduli.login_bot import accedi_e_salva_html
from moduli.parser import estrai_e_salva_turni_csv
from moduli.analisi_turni import unisci_turni_e_salva
import time

def main():

    for nome, dati in UTENTI.items():
        print(f"\n🔐 Accesso per {nome}")
        accedi_e_salva_html(dati["username"], dati["password"], dati["html_path"])
        estrai_e_salva_turni_csv(dati["html_path"], dati["csv_path"])
        time.sleep(5)

    unisci_turni_e_salva()

    # fine di main.py, dopo unisci_turni_e_salva()
    import subprocess, os

    # path relativo al repo Git
    CSV_PATH = "dati/turni_csv/turni_uniti.csv"
    os.chdir(os.path.dirname(__file__))  # assicurati di stare nella root del repo
    subprocess.run(["git", "add", CSV_PATH])
    subprocess.run(["git", "commit", "-m", "🗓️ Aggiornamento turni"])
    subprocess.run(["git", "push"])

    # Chiedi se aprire l'app Web
    apri = input("Vuoi aprire l'app Web? [1/2]: ")
    if apri.strip().lower() == "1":
        import webbrowser
        webbrowser.open("https://turni-valerio-sirya.streamlit.app/")

if __name__ == "__main__":
    main()
