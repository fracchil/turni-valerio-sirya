from pywinauto.application import Application
import pywinauto.keyboard as keyboard
import pyautogui
import time
import os
import pyperclip
import pygetwindow as gw

def accedi_e_salva_html(username, password, output_path):
    print(f"🚀 Login per {username}...")
    os.startfile("chrome.exe")
    time.sleep(3)  # aspetta che Chrome si apra

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
    time.sleep(2.5)

    pyautogui.write(username)
    pyautogui.press("tab")
    time.sleep(0.5)
    pyautogui.write(password)
    pyautogui.press("enter")
    print("🎯 Login completato")
    time.sleep(2)

    pyautogui.press("f12")
    time.sleep(1)
    pyautogui.press("f2")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    pyautogui.press("f12")
    time.sleep(1)

    html = pyperclip.paste()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ DOM salvato in '{output_path}'")
    
    logout_path = os.path.join(os.path.dirname(__file__), "logout_button.png")
    btn = pyautogui.locateCenterOnScreen(logout_path, confidence=0.9)

    if btn:
        pyautogui.click(btn)
        print("🔓 Logout effettuato")
        pyautogui.press("enter")
        time.sleep(1)
    else:
        print("⚠️ Logout non trovato a schermo")
