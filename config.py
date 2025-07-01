# utilizzato in analisi
percorso_csv_valerio = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/turni_csv/turni_valerio.csv"
percorso_csv_sirya   = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/turni_csv/turni_sirya.csv"
percorso_csv_uniti = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/turni_csv/turni_uniti.csv"
LOGIN_URL = "https://www.webcrew.trenitalia.it/mbweb/main/trenitalia/desktop/main-menu"
# config.py per github
PER_CSV = "https://raw.githubusercontent.com/fracchil/turni-valerio-sirya/refs/heads/main/dati/turni_csv/turni_uniti.csv"

UTENTI = {
    "valerio": {
        "username": "2956230",
        "password": "Parrucchino39",
        "html_path": "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/raw_html/valerio.html", #percorso salvataggio html
        "csv_path":  percorso_csv_valerio #percorso salvataggio csv
    },
    "sirya": {
        "username": "2955789",
        "password": "250508.Cc",
        "html_path": "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/raw_html/sirya.html",
        "csv_path": percorso_csv_sirya
    }
}




'''
# Percorsi dei file
input_path = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/turni_uniti.csv"
output_path = "C:/Users/valer/Documents/Progammazione/Python/Lettore_turno/dati/consigli_giornalieri.csv"
'''