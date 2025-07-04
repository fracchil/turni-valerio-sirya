import subprocess
import os

def aggiorna_git():
    os.chdir(os.path.dirname(__file__))  # Vai nella root del progetto
    # Trova i file modificati o aggiunti
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    changed_files = []
    for line in result.stdout.splitlines():
        if line and (line.startswith(' M') or line.startswith('A ') or line.startswith('??')):
            file_path = line[3:]
            changed_files.append(file_path)
    if not changed_files:
        print("Nessun file modificato da aggiornare.")
        return
    print("File da aggiornare:")
    for f in changed_files:
        print(f" - {f}")
    # Chiedi il messaggio di commit
    commit_msg = input("Scrivi il messaggio per il commit: ")
    # Aggiungi tutte le modifiche (inclusi file eliminati e nuovi)
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push"])
    print("✅ Aggiornamento completato!")

if __name__ == "__main__":
    aggiorna_git()
