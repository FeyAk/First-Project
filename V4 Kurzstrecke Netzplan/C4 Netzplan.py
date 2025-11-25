# Netzwerk-Daten
UB_NETZ = {
    "Fürth Hbf.": ["Jakobinenstr."],
    "Jakobinenstr.": ["Fürth Hbf.", "Stadtgrenze"],
    "Stadtgrenze": ["Jakobinenstr.", "Muggenhof"],
    "Muggenhof": ["Stadtgrenze", "EberhardsHof"],
    "EberhardsHof": ["Muggenhof", "Maximilianstr."],
    "Maximilianstr.": ["EberhardsHof", "Bärenschanze"],
    "Bärenschanze": ["Maximilianstr.", "Gostenhof"],
    "Gostenhof": ["Bärenschanze", "Plärrer"],
    "Gustav-Adolf-Str.": ["Sündersbühl"],
    "Sündersbühl": ["Gustav-Adolf-Str.", "Rothenburger Str."],
    "Plärrer": ["Rothenburger Str.", "Gostenhof", "Weißer Turm", "Opernhaus"],
    "Rothenburger Str.": ["Sündersbühl", "Plärrer", "St. Leonhard"],
    "Weißer Turm": ["Plärrer", "Lorenzkirche"],
    "Lorenzkirche": ["Weißer Turm", "Hauptbahnhof"],
    "Opernhaus": ["Plärrer", "Hauptbahnhof"],
    "Hauptbahnhof": ["Lorenzkirche", "Opernhaus", "Aufseßplatz", "Wöhrder Wiese"],
    "St. Leonhard": ["Rothenburger Str.", "Schweinau"],
    "Schweinau": ["St. Leonhard", "Hohe Marter"],
    "Hohe Marter": ["Schweinau", "Röthenbach"],
    "Röthenbach": ["Hohe Marter"],
    "Wöhrder Wiese": ["Hauptbahnhof", "Rathenauplatz"],
    "Rathenauplatz": ["Wöhrder Wiese", "Rennweg", "Maxfeld"],
    "Rennweg": ["Rathenauplatz", "Schoppershof"],
    "Schoppershof": ["Rennweg", "Nordostbahnhof"],
    "Nordostbahnhof": ["Schoppershof", "Herrnhütte"],
    "Herrnhütte": ["Nordostbahnhof", "Ziegelstein"],
    "Ziegelstein": ["Herrnhütte", "Flughafen"],
    "Flughafen": ["Ziegelstein"],
    "Aufseßplatz": ["Hauptbahnhof", "Maffeiplatz"],
    "Maffeiplatz": ["Aufseßplatz", "Frankenstr."],
    "Frankenstr.": ["Maffeiplatz", "Hasenbuck"],
    "Hasenbuck": ["Frankenstr.", "Bauernfeindstr."],
    "Bauernfeindstr.": ["Hasenbuck", "Messe"],
    "Messe": ["Bauernfeindstr.", "Langwasser Nord"],
    "Langwasser Nord": ["Messe", "Scharfreiterring"],
    "Scharfreiterring": ["Langwasser Nord", "Langwasser Mitte"],
    "Langwasser Mitte": ["Scharfreiterring", "Gemeinschaftshaus"],
    "Gemeinschaftshaus": ["Langwasser Mitte", "Langwasser Süd"],
    "Langwasser Süd": ["Gemeinschaftshaus"],
    "Fr.-Ebert-Platz": ["Kaulbachplatz"],
    "Kaulbachplatz": ["Fr.-Ebert-Platz", "Maxfeld"],
    "Maxfeld": ["Kaulbachplatz", "Rathenauplatz"],
}

ALLE_STATIONEN = list(UB_NETZ.keys())

U1_LINIE = ["Fürth Hbf.", "Jakobinenstr.", "Stadtgrenze", "Muggenhof", "EberhardsHof",
            "Maximilianstr.", "Bärenschanze", "Gostenhof", "Plärrer", "Weißer Turm",
            "Lorenzkirche", "Hauptbahnhof", "Aufseßplatz", "Maffeiplatz", "Frankenstr.",
            "Hasenbuck", "Bauernfeindstr.", "Messe", "Langwasser Nord", "Scharfreiterring",
            "Langwasser Mitte", "Gemeinschaftshaus", "Langwasser Süd"]

U2_LINIE = ["Flughafen", "Ziegelstein", "Herrnhütte", "Nordostbahnhof", "Schoppershof",
            "Rennweg", "Rathenauplatz", "Wöhrder Wiese", "Hauptbahnhof", "Opernhaus",
            "Plärrer", "Rothenburger Str.", "St. Leonhard", "Schweinau", "Hohe Marter", "Röthenbach"]

U3_LINIE = ["Gustav-Adolf-Str.", "Sündersbühl", "Rothenburger Str.", "Plärrer", "Weißer Turm",
            "Lorenzkirche", "Hauptbahnhof", "Opernhaus", "Wöhrder Wiese", "Rathenauplatz",
            "Maxfeld", "Kaulbachplatz", "Fr.-Ebert-Platz"]

UMSTEIGEPUNKTE = ["Plärrer", "Hauptbahnhof", "Nordostbahnhof", "St. Leonhard", "Opernhaus", "Maffeistr."]

# Imports
from datetime import datetime
import sys, time, os
from colorama import init, Fore, Style
import winsound

try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

init(autoreset=True, convert=True)


def finde_kuerzesten_pfad(start, ziel):
    if start not in UB_NETZ or ziel not in UB_NETZ or start == ziel:
        return [start] if start == ziel else None

    warteschlange = [(start, [start])]
    besucht = {start}

    while warteschlange:
        akt_station, pfad = warteschlange.pop(0)
        for nachbar in UB_NETZ.get(akt_station, []):
            if nachbar == ziel:
                return pfad + [ziel]
            if nachbar not in besucht:
                besucht.add(nachbar)
                warteschlange.append((nachbar, pfad + [nachbar]))
    return None


def play_sound(sound_type):
    try:
        sounds = {
            "startup": [(392, 150), (523, 150), (659, 150), (784, 250)],
            "success": [(523, 150), (659, 150), (784, 200)],
            "complete": [(523, 150), (659, 150), (784, 150), (1047, 400)],
            "click": [(800, 80)],
            "error": None
        }
        if sound_type == "error":
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        elif sound_type in sounds:
            for freq, dur in sounds[sound_type]:
                winsound.Beep(freq, dur)
                time.sleep(0.05)
    except:
        pass


def print_slow(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(dauer=1.5, text="Suche kürzeste Route..."):
    syms = ['|', '/', '-', '\\']
    start = time.time()
    i = 0
    while time.time() - start < dauer:
        sys.stdout.write(Fore.YELLOW + f'\r{text} {syms[i % 4]}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * (len(text) + 2) + '\r')


def zeige_netzplan():
    for name in ["netzplan.png"]:
        if os.path.exists(name) and PIL_AVAILABLE:
            try:
                print_slow(Fore.GREEN + f"🗺️  Öffne Netzplan ({name})...")
                Image.open(name).show()
                print_slow(Fore.GREEN + "✔️ Netzplan wird in separatem Fenster angezeigt.")
                time.sleep(1)
                return
            except:
                pass


def hole_stationen_geordnet():
    stationen, gesehen = [], set()
    for station in U1_LINIE + U2_LINIE + U3_LINIE:
        if station not in gesehen and station in ALLE_STATIONEN:
            stationen.append(station)
            gesehen.add(station)
    return stationen


def zeige_stationen_liste():
    print_slow(Fore.CYAN + "\nVerfügbare Stationen (nach Linien geordnet):")
    print_slow(Fore.YELLOW + "═" * 60)

    counter = 1
    for linie, name, anzahl in [(U1_LINIE, "U1-Linie (Fürth Hbf. ↔ Langwasser Süd)", 23),
                                (U2_LINIE, "U2-Linie (Flughafen ↔ Röthenbach)", 16),
                                (U3_LINIE, "U3-Linie (Gustav-Adolf-Str. ↔ Fr.-Ebert-Platz)", 13)]:
        print_slow(Fore.RED + Style.BRIGHT + f"\n🚇 {name} - {anzahl} Stationen")
        print_slow(Fore.YELLOW + "—" * 60)

        # Nur neue Stationen anzeigen (außer U1)
        bereits_gezeigt = set() if linie == U1_LINIE else set(U1_LINIE + (U2_LINIE if linie == U3_LINIE else []))

        for station in linie:
            if station in ALLE_STATIONEN and station not in bereits_gezeigt:
                print_slow(Fore.CYAN + f"  {counter:2}. {station}")
                counter += 1

    print_slow(Fore.YELLOW + "═" * 60)
    print_slow(Fore.WHITE + f"Gesamt: {len(hole_stationen_geordnet())} eindeutige Stationen\n")


def erfrage_station(aufforderung):
    stationen = hole_stationen_geordnet()
    while True:
        eingabe = input(Fore.CYAN + aufforderung + Style.RESET_ALL).strip()

        if eingabe.isdigit():
            nummer = int(eingabe)
            if 1 <= nummer <= len(stationen):
                play_sound("click")
                return stationen[nummer - 1]
            print_slow(Fore.RED + f"❌ Nummer {nummer} ungültig. Bitte 1-{len(stationen)} wählen.")
            play_sound("error")
        elif eingabe in ALLE_STATIONEN:
            play_sound("click")
            return eingabe
        else:
            print_slow(Fore.RED + f"❌ '{eingabe}' unbekannt. Bitte erneut versuchen.")
            play_sound("error")


def erfrage_ja_nein(frage):
    while True:
        antwort = input(Fore.MAGENTA + f"{frage} (j/n): " + Style.RESET_ALL).strip().lower()
        if antwort in ('j', 'n'):
            play_sound("click")
            return antwort == 'j'
        print_slow(Fore.RED + "❌ Bitte nur 'j' oder 'n' eingeben.")
        play_sound("error")


def berechne_preis(distanz, ermaessigt, bar, einzelfahrt):
    grundpreis = 2.50 if distanz <= 3 else 5.00
    ticket_typ = "Kurzstrecke" if distanz <= 3 else "Langstrecke"

    # Entscheidungstabelle
    regeln = [
        (True, False, False, 20, 0),  # R1
        (True, True, False, 20, 10),  # R2
        (True, False, True, 20, 5),  # R3
        (True, True, True, 20, 15),  # R4
        (False, False, False, 0, 0),  # R5
        (False, True, False, 0, 10),  # R6
        (False, False, True, 0, 5),  # R7
        (False, True, True, 0, 15),  # R8
    ]

    for i, (e, b, ei, rab, zus) in enumerate(regeln, 1):
        if (e, b, ei) == (ermaessigt, bar, einzelfahrt):
            rabatt_betrag = grundpreis * (rab / 100)
            zuschlag_betrag = grundpreis * (zus / 100)
            return {
                'grundpreis': grundpreis, 'ticket_typ': ticket_typ,
                'rabatt_prozent': rab, 'rabatt_betrag': rabatt_betrag,
                'zuschlag_prozent': zus, 'zuschlag_betrag': zuschlag_betrag,
                'endpreis': grundpreis - rabatt_betrag + zuschlag_betrag,
                'regel': f"R{i}"
            }


def zeige_entscheidungstabelle(ermaessigt, bar, einzelfahrt, aktive_regel):
    print_slow(Fore.YELLOW + "\n" + "═" * 85)
    print_slow(Fore.WHITE + Style.BRIGHT + "VERWENDETE ENTSCHEIDUNGSTABELLE")
    print_slow(Fore.YELLOW + "═" * 85)

    print(
        Fore.CYAN + Style.BRIGHT + f"{'R':<32}{'R1':<9}{'R2':<9}{'R3':<9}{'R4':<9}{'R5':<9}{'R6':<9}{'R7':<9}{'R8':<9}")
    print(Fore.YELLOW + "-" * 85)

    def zeile(label, werte):
        line = f"  {label:<30}"
        for i, w in enumerate(werte, 1):
            line += (Fore.GREEN + Style.BRIGHT if f"R{i}" == aktive_regel else "") + f"{w:<9}" + (
                Style.RESET_ALL if f"R{i}" == aktive_regel else "")
        return line

    print(zeile("Ermäßigungsberechtigt?", ["j", "j", "j", "j", "n", "n", "n", "n"]))
    print(zeile("Zahlungsart = Bar?", ["n", "j", "n", "j", "n", "j", "n", "j"]))
    print(zeile("Ticketart = Einzelfahrt?", ["n", "n", "j", "j", "n", "n", "j", "j"]))

    print(Fore.YELLOW + "-" * 85)
    print(Fore.CYAN + Style.BRIGHT + f"{'Aktion':<32}")
    print(Fore.YELLOW + "-" * 85)

    print(zeile("Rabatt 20%", ["x", "x", "x", "x", "-", "-", "-", "-"]))
    print(zeile("Zuschlag 5%", [" ", " ", "x", " ", " ", " ", "x", " "]))
    print(zeile("Zuschlag 10%", [" ", "x", " ", " ", " ", "x", " ", " "]))
    print(zeile("Zuschlag 15%", [" ", " ", " ", "x", " ", " ", " ", "x"]))

    print(Fore.YELLOW + "═" * 85)
    print(Fore.GREEN + Style.BRIGHT + f"→ Angewendete Regel: {aktive_regel}")
    print(Fore.YELLOW + "═" * 85)


def starte_fahrkarten_automat():
    print(Fore.YELLOW + "🔊 Starte System...")
    play_sound("startup")
    time.sleep(0.3)

    print_slow(Fore.YELLOW + "═" * 60)
    print_slow(Fore.GREEN + Style.BRIGHT + "🚆 Intelligenter Fahrkartenautomat U-Bahn Netz 🚇")
    print_slow(Fore.YELLOW + "═" * 60)

    print()
    zeige_netzplan()
    print()
    zeige_stationen_liste()

    print_slow(Fore.BLUE + "\n--- Routenplanung ---")
    print_slow(Fore.WHITE + "Tipp: Geben Sie die Nummer oder den Namen der Station ein")

    start_station = erfrage_station("\nStartstation (Nummer oder Name): ")
    print_slow(Fore.GREEN + f"✔️ Start: {start_station}")

    ziel_station = erfrage_station("Zielstation (Nummer oder Name): ")
    print_slow(Fore.GREEN + f"✔️ Ziel: {ziel_station}")

    spinner(dauer=1.5)
    route = finde_kuerzesten_pfad(start_station, ziel_station)

    if not route:
        print_slow(Fore.RED + f"\n❌ Keine Route gefunden!")
        play_sound("error")
        sys.exit(1)
    genutzte_umsteigepunkte = [station for station in route if station in UMSTEIGEPUNKTE]
    if genutzte_umsteigepunkte:
        print_slow(Fore.MAGENTA + f"🔄 Umsteigepunkte: {', '.join(genutzte_umsteigepunkte)}")

    anzahl_stationen = len(route) - 1
    print_slow(Fore.GREEN + f"✅ Route gefunden! Dauer: {anzahl_stationen} Stationen.")
    play_sound("success")

    print_slow(Fore.BLUE + "\n--- Rabatt- & Zuschlagsoptionen ---")
    print_slow(Fore.WHITE + "Bitte mit 'j' für Ja oder 'n' für Nein antworten:\n")

    ermaessigt = erfrage_ja_nein("1. Ermäßigungsberechtigt?")
    bar = erfrage_ja_nein("2. Barzahlung?")
    einzelfahrt = erfrage_ja_nein("3. Einzelfahrt?")

    preis_info = berechne_preis(anzahl_stationen, ermaessigt, bar, einzelfahrt)

    print_slow(Fore.YELLOW + "\n" + "═" * 60)
    print_slow(Fore.WHITE + Style.BRIGHT + "🎫 IHR FAHRSCHEIN (Quittung) 🎫")
    print_slow(Fore.YELLOW + "═" * 60)

    print_slow(Fore.WHITE + f"Von:      {start_station}")
    print_slow(Fore.WHITE + f"Nach:     {ziel_station}")
    print_slow(Fore.WHITE + f"Distanz:  {anzahl_stationen} Station(en)")
    print_slow(Fore.YELLOW + "-" * 60)

    print_slow(Fore.CYAN + "Passierte Stationen:")
    sys.stdout.write(Fore.CYAN + " " * 4)
    sys.stdout.flush()

    for i, station in enumerate(route):
        color = Fore.YELLOW + Style.BRIGHT if station in UMSTEIGEPUNKTE else Fore.CYAN
        sys.stdout.write(color + station + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.15)
        if i < len(route) - 1:
            sys.stdout.write(Fore.WHITE + " → ")
            sys.stdout.flush()
            time.sleep(0.08)

    print()
    print_slow(Fore.YELLOW + "-" * 60)

    print_slow(Fore.CYAN + f"Ticket:       {preis_info['ticket_typ']}")
    print_slow(Fore.CYAN + f"Grundpreis:   €{preis_info['grundpreis']:.2f}")

    if preis_info['rabatt_prozent'] > 0:
        print_slow(Fore.GREEN + f"Rabatt ({preis_info['rabatt_prozent']}%):   -€{preis_info['rabatt_betrag']:.2f}")

    if preis_info['zuschlag_prozent'] > 0:
        print_slow(Fore.RED + f"Zuschlag ({preis_info['zuschlag_prozent']}%): +€{preis_info['zuschlag_betrag']:.2f}")

    print_slow(Fore.YELLOW + "—" * 60)
    print_slow(Fore.WHITE + Style.BRIGHT + f"ENDPREIS:     €{preis_info['endpreis']:.2f}")
    print_slow(Fore.MAGENTA + f"\nGültig ab: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print_slow(Fore.YELLOW + "═" * 60)

    zeige_entscheidungstabelle(ermaessigt, bar, einzelfahrt, preis_info['regel'])

    play_sound("complete")
    print_slow(Fore.GREEN + "\n✅ Vielen Dank für Ihre Buchung! Gute Fahrt! 🚇")


if __name__ == "__main__":
    starte_fahrkarten_automat()
