from pywinauto.application import Application
import pywinauto.keyboard as keyboard
import pyautogui
import time
import os
import pyperclip
import pygetwindow as gw


# Funzione per ottenere il percorso assoluto di un'immagine nella cartella img
def get_img_path(filename):
    return os.path.join(os.path.dirname(__file__), "img", filename)


# Funzione per attendere la comparsa di un'immagine sullo schermo
def wait_for_image(image_path, timeout=20, confidence=0.9):
    """Attende che l'immagine compaia sullo schermo entro timeout secondi."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if pos:
                return pos
        except Exception as e:
            print(f"[wait_for_image] Warning: {e}")
        time.sleep(0.5)
    raise TimeoutError(f"Elemento {image_path} non trovato entro {timeout} secondi.")


def accedi_e_salva_html(username, password, output_path):
    print(f"🚀 Login per {username}...")
    os.startfile("chrome.exe")
    wait_for_image(get_img_path("identifica_chrome.png"), timeout=10, confidence=0.7)
    for w in gw.getWindowsWithTitle("Chrome"):
        try:
            w.maximize()
            print("🪟 Finestra Chrome massimizzata!")
            break
        except:
            print("⚠️ Impossibile massimizzare finestra.")
    
    LOGIN_URL = "https://www.webcrew.trenitalia.it/mbweb/main/trenitalia/desktop/main-menu"
    pyperclip.copy(LOGIN_URL)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    wait_for_image(get_img_path("identifica_username.png"), timeout=10, confidence=0.7)
    pyautogui.write(username)
    pyautogui.press("tab")
    time.sleep(0.25)
    pyautogui.write(password)
    pyautogui.press("enter")
    print("🎯 Login completato")
    wait_for_image(get_img_path("identifica_accesso.png"), timeout=10, confidence=0.7)
    pyautogui.press("f12")
    wait_for_image(get_img_path("identifica_f12.png"), timeout=10, confidence=0.7)
    pyautogui.press("f2")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    pyautogui.press("f12")
    wait_for_image(get_img_path("logout_button.png"), timeout=10, confidence=0.7)

    html = pyperclip.paste()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ DOM salvato in '{output_path}'")
    logout_path = get_img_path("logout_button.png")
    btn = pyautogui.locateCenterOnScreen(logout_path, confidence=0.9)

    if btn:
        pyautogui.click(btn)
        print("🔓 Logout effettuato")
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "w")
    else:
        print("⚠️ Logout non trovato a schermo")