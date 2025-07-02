import pandas as pd
import os
from datetime import datetime, timedelta, time
from config import percorso_csv_valerio, percorso_csv_sirya, percorso_csv_uniti

DAY_IT = {
    "Monday":    "Lunedì",
    "Tuesday":   "Martedì",
    "Wednesday": "Mercoledì",
    "Thursday":  "Giovedì",
    "Friday":    "Venerdì",
    "Saturday":  "Sabato",
    "Sunday":    "Domenica"
}

def parse_ora(ora_str, giorno_base, inizio_ref=None):
    if pd.isna(ora_str):
        return None, False
    s = ora_str.strip()
    plus = "+" in s
    s = s.replace("+", "")
    try:
        t = datetime.strptime(s, "%H:%M").time()
    except ValueError:
        return None, False
    if inizio_ref and not plus and t <= inizio_ref.time():
        plus = True
    giorno = giorno_base.date() + (timedelta(days=1) if plus else timedelta())
    return datetime.combine(giorno, t), plus

def crea_mappa_turni_e_testo(df):
    mappa, testo = {}, {}
    for _, r in df.iterrows():
        d0 = r["Data"].date()
        tipo = str(r.get("Tipo", "")).strip().lower()
        s0, _ = parse_ora(r.get("Ora Inizio"), r["Data"])
        e0, plus = parse_ora(r.get("Ora Fine"), r["Data"], inizio_ref=s0)

        if s0 and e0:
            if not plus:
                mappa.setdefault(d0, []).append((s0, e0))
                testo.setdefault(d0, f"{s0.strftime('%H:%M')}-{e0.strftime('%H:%M')}")
            else:
                eod = datetime.combine(d0, time(23,59,59))
                mappa.setdefault(d0, []).append((s0, eod))
                testo.setdefault(d0, f"{s0.strftime('%H:%M')}-{eod.strftime('%H:%M')}")
                d1 = d0 + timedelta(days=1)
                md = datetime.combine(d1, time(0,0))
                mappa.setdefault(d1, []).append((md, e0))
                seg = f"00:00-{e0.strftime('%H:%M')}"
                testo[d1] = (testo.get(d1,"") + "; " if testo.get(d1) else "") + seg
            continue

        if tipo.startswith("riposo") or tipo.startswith("intervallo") or tipo in ("n/d","libero"):
            mappa.setdefault(d0, [])
            testo.setdefault(d0, r["Tipo"])
            continue

        if "in modifica" in tipo or "disp" in tipo:
            mappa[d0] = None
            testo.setdefault(d0, r["Tipo"])
            continue

        mappa[d0] = None
        testo.setdefault(d0, r["Tipo"] or "N/D")

    return mappa, testo

def intervallo_libero(occ, giorno):
    occ = occ or []
    occ.sort()
    start = datetime.combine(giorno, time(0, 0))
    endd  = datetime.combine(giorno, time(23,59,59))
    lib = []
    cur = start
    for a, b in occ:
        if a > cur:
            lib.append((cur, a))
        cur = max(cur, b)
    if cur < endd:
        lib.append((cur, endd))
    return lib

def intersezione(a1, a2):
    out = []
    for s1, e1 in a1:
        for s2, e2 in a2:
            s, e = max(s1, s2), min(e1, e2)
            if s < e:
                out.append((s, e))
    return out

def overlap_secs(s, e, ws, we):
    start = max(s, ws)
    end = min(e, we)
    return max((end - start).total_seconds(), 0)

def analizza_fascia(comuni):
    if not comuni:
        return "🔸 Tempo parziale (<3h utili)"

    day = comuni[0][0].date()
    # giornata utile: solo dopo le 08:00
    day_start = datetime.combine(day, time(8,0))
    day_end   = datetime.combine(day, time(23,59,59))

    intervalli_utili = []
    for s, e in comuni:
        inizio = max(s, day_start)
        fine = min(e, day_end)
        if inizio < fine:
            intervalli_utili.append((inizio, fine))

    ore_disponibili = sum((f - i).total_seconds() for i, f in intervalli_utili) / 3600
    if ore_disponibili >= 13:
        return "🌞 Giornata piena disponibile!"

    # Fasce standard
    ms, me = datetime.combine(day, time(8,0)),  datetime.combine(day, time(13,0))
    ps, pe = datetime.combine(day, time(13,0)), datetime.combine(day, time(19,0))
    es, ee = datetime.combine(day, time(19,0)), datetime.combine(day, time(23,59,59))

    m_h = sum(overlap_secs(s, e, ms, me) for s, e in comuni) / 3600
    p_h = sum(overlap_secs(s, e, ps, pe) for s, e in comuni) / 3600
    e_h = sum(overlap_secs(s, e, es, ee) for s, e in comuni) / 3600

    matt = m_h >= 3
    pom  = p_h >= 3
    sera = e_h >= 3

    for s, e in comuni:
        bs, be = max(s, ms), min(e, pe)
        dur = (be - bs).total_seconds() / 3600 if be > bs else 0
        mh = overlap_secs(s, e, ms, me) / 3600
        ph = overlap_secs(s, e, ps, pe) / 3600
        if dur >= 6 and mh >= 3 and ph >= 3:
            return "⚡ Matteriggio libero!"

    for s, e in comuni:
        bs, be = max(s, ps), min(e, ee)
        dur = (be - bs).total_seconds() / 3600 if be > bs else 0
        ph = overlap_secs(s, e, ps, pe) / 3600
        eh = overlap_secs(s, e, es, ee) / 3600
        if dur >= 6 and ph >= 3 and eh >= 3:
            return "🔥 Pomesera libero!"

    if matt and sera and not pom:
        return "🕗 Mattina + 🌇 Sera"
    if matt:
        return "🕗 Mattina"
    if pom:
        return "🌅 Solo pomeriggio"
    if sera:
        return "🌇 Sera"
    if any(s.time() < time(8,0) or e.time() > time(23,0) for s, e in comuni):
        return "🌙 Solo notte disponibile"

    return "🔸 Tempo parziale (<3h utili)"

def unisci_turni_e_salva():
    val = pd.read_csv(percorso_csv_valerio); val["Data"] = pd.to_datetime(val["Data"])
    sir = pd.read_csv(percorso_csv_sirya);   sir["Data"] = pd.to_datetime(sir["Data"])

    m_v, t_v = crea_mappa_turni_e_testo(val)
    m_s, t_s = crea_mappa_turni_e_testo(sir)
    all_days = sorted(set(m_v.keys()) | set(m_s.keys()))

    out = []
    for d in all_days:
        occ_v = m_v.get(d, []); txt_v = t_v.get(d, "Libero") if occ_v is not None else "N/D"
        occ_s = m_s.get(d, []); txt_s = t_s.get(d, "Libero") if occ_s is not None else "N/D"

        if occ_v is None or occ_s is None:
            fascia = "Non calcolabile"
            sint   = "—"
        else:
            lv   = intervallo_libero(occ_v, d)
            ls   = intervallo_libero(occ_s, d)
            comuni = intersezione(lv, ls)
            fascia = "Nessuna" if not comuni else "; ".join(f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}" for s,e in comuni)
            sint   = analizza_fascia(comuni)

        out.append({
            "Data": d.strftime("%Y-%m-%d"),
            "Giorno": DAY_IT[d.strftime("%A")],
            "Turno Valerio": txt_v,
            "Turno Sirya": txt_s,
            "Fascia Libera Comune": fascia,
            "Fascia Libera Sintetica": sint
        })

    os.makedirs(os.path.dirname(percorso_csv_uniti), exist_ok=True)
    pd.DataFrame(out).to_csv(percorso_csv_uniti, index=False, encoding="utf-8")
    print("✅ File creato in:", percorso_csv_uniti)

if __name__ == "__main__":
    unisci_turni_e_salva()
