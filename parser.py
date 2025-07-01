from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def estrai_e_salva_turni_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    giorni = soup.select("td.day")
    dati_turni = []

    for giorno in giorni:
        data_tag = giorno.select_one(".date")
        if not data_tag:
            continue

        data_str = data_tag.text.strip()
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%y")
            data_iso = data_obj.date().isoformat()
        except ValueError:
            continue

        duty_code = giorno.select_one(".duty-nr")
        nome_descrizione = giorno.select_one(".allocation-name")
        ora_inizio = giorno.select_one(".time.begin")
        luogo_inizio = giorno.select_one(".location.begin")
        ora_fine = giorno.select_one(".time.end")
        luogo_fine = giorno.select_one(".location.end")

        tipo = ""
        if duty_code:
            tipo = "Lavoro"
        elif nome_descrizione:
            tipo = nome_descrizione.text.strip()
        elif giorno.select_one(".caption"):
            tipo = giorno.select_one(".caption").text.strip()
        else:
            tipo = "N/D"

        dati_turni.append({
            "Data": data_iso,
            "Tipo": tipo,
            "Turno": duty_code.text.strip() if duty_code else "",
            "Ora Inizio": ora_inizio.text.strip() if ora_inizio else "",
            "Luogo Inizio": luogo_inizio.text.strip() if luogo_inizio else "",
            "Ora Fine": ora_fine.text.strip() if ora_fine else "",
            "Luogo Fine": luogo_fine.text.strip() if luogo_fine else ""
        })

    # Salvataggio in CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dati_turni[0].keys())
        writer.writeheader()
        writer.writerows(dati_turni)

    print(f"✅ Turni salvati in {output_path} ({len(dati_turni)} giorni)")