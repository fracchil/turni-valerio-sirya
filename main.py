from config import UTENTI
from login_bot import accedi_e_salva_html
from parser import estrai_e_salva_turni_csv
from analisi_turni import unisci_turni_e_salva
import time

def main():
    scelta = input(
        "Scegli modalità:\n"
        "1) Scarica e analizza turni\n"
        "2) Solo analizza (usa i file CSV già presenti)\n> "
    )

    if scelta == "1":
        for nome, dati in UTENTI.items():
            print(f"\n🔐 Accesso per {nome}")
            accedi_e_salva_html(dati["username"], dati["password"], dati["html_path"])
            estrai_e_salva_turni_csv(dati["html_path"], dati["csv_path"])
            time.sleep(8)

        unisci_turni_e_salva()

        # fine di main.py, dopo unisci_turni_e_salva()
        import subprocess, os

        # path relativo al repo Git
        CSV_PATH = "dati/turni_uniti.csv"
        os.chdir(os.path.dirname(__file__))  # assicurati di stare nella root del repo
        subprocess.run(["git", "add", CSV_PATH])
        subprocess.run(["git", "commit", "-m", "🗓️ Aggiornamento turni"])
        subprocess.run(["git", "push"])

    elif scelta == "2":
        unisci_turni_e_salva()

    else:
        print("❌ Scelta non valida.")

if __name__ == "__main__":
    main()
