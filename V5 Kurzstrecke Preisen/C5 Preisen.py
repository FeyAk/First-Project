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

UMSTEIGEPUNKTE = ["Plärrer", "Hauptbahnhof", "Rothenburger Str.", "Wöhrder Wiese", "Rathenauplatz", "Opernhaus"]

# Ticket-Preise
TICKETPREISE = {
    'Kurz': {'Einzel': 1.50, 'Mehrfahrt': 5.00},
    'Mittel': {'Einzel': 2.00, 'Mehrfahrt': 7.00},
    'Lang': {'Einzel': 3.00, 'Mehrfahrt': 10.00}
}

# Imports
from datetime import datetime, timedelta
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


def bestimme_ticketkategorie(anzahl_stationen):
    """Bestimmt die Ticketkategorie basierend auf der Stationsanzahl"""
    if anzahl_stationen <= 3:
        return 'Kurz'
    elif anzahl_stationen <= 8:
        return 'Mittel'
    else:
        return 'Lang'


def zeige_verfuegbare_tickets(anzahl_stationen):
    """Zeigt verfügbare Ticketoptionen basierend auf der Stationsanzahl"""
    print_slow(Fore.BLUE + "\n--- Verfügbare Tickets für Ihre Route ---")
    print_slow(Fore.YELLOW + "═" * 60)

    print_slow(Fore.CYAN + f"Ihre Route umfasst {anzahl_stationen} Station(en).\n")

    if anzahl_stationen <= 3:
        print_slow(Fore.GREEN + "✓ Kurzticket (1-3 Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €1,50")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €5,00\n")

        print_slow(Fore.GREEN + "✓ Mittelticket (1-8 Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €2,00")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €7,00\n")

        print_slow(Fore.GREEN + "✓ Langticket (beliebig viele Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €3,00")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €10,00")

    elif anzahl_stationen <= 8:
        print_slow(Fore.RED + "✗ Kurzticket (1-3 Stationen) - NICHT AUSREICHEND\n")

        print_slow(Fore.GREEN + "✓ Mittelticket (1-8 Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €2,00")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €7,00\n")

        print_slow(Fore.GREEN + "✓ Langticket (beliebig viele Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €3,00")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €10,00")

    else:
        print_slow(Fore.RED + "✗ Kurzticket (1-3 Stationen) - NICHT AUSREICHEND")
        print_slow(Fore.RED + "✗ Mittelticket (1-8 Stationen) - NICHT AUSREICHEND\n")

        print_slow(Fore.GREEN + "✓ Langticket (beliebig viele Stationen) - VERFÜGBAR")
        print_slow(Fore.WHITE + "  • Einzelticket: €3,00")
        print_slow(Fore.WHITE + "  • Mehrfahrtenticket (4x): €10,00")

    print_slow(Fore.YELLOW + "═" * 60)


def erfrage_ticketwahl(anzahl_stationen):
    """Fragt Ticketkategorie und Ticketart ab"""
    empfohlene_kategorie = bestimme_ticketkategorie(anzahl_stationen)

    # Ticketkategorie wählen
    print_slow(Fore.YELLOW + "\n" + "═" * 60)
    print_slow(Fore.BLUE + Style.BRIGHT + "SCHRITT 1: TICKETKATEGORIE WÄHLEN")
    print_slow(Fore.YELLOW + "═" * 60)
    print_slow(Fore.GREEN + f"💡 Empfehlung für {anzahl_stationen} Station(en): {empfohlene_kategorie}ticket")
    print_slow(Fore.YELLOW + "─" * 60)

    while True:
        if anzahl_stationen <= 3:
            print_slow(Fore.WHITE + "\n  [1] Kurzticket (1-3 Stationen)   - Einzel: €1,50 / Mehrfahrt: €5,00")
            print_slow(Fore.WHITE + "  [2] Mittelticket (1-8 Stationen) - Einzel: €2,00 / Mehrfahrt: €7,00")
            print_slow(Fore.WHITE + "  [3] Langticket (beliebig)        - Einzel: €3,00 / Mehrfahrt: €10,00")
            gueltige_optionen = ['1', '2', '3']
        elif anzahl_stationen <= 8:
            print_slow(Fore.WHITE + "\n  [2] Mittelticket (1-8 Stationen) - Einzel: €2,00 / Mehrfahrt: €7,00")
            print_slow(Fore.WHITE + "  [3] Langticket (beliebig)        - Einzel: €3,00 / Mehrfahrt: €10,00")
            gueltige_optionen = ['2', '3']
        else:
            print_slow(Fore.WHITE + "\n  [3] Langticket (beliebig)        - Einzel: €3,00 / Mehrfahrt: €10,00")
            gueltige_optionen = ['3']

        print_slow(Fore.YELLOW + "\n→ Bitte geben Sie die Nummer ein (z.B. '3' für Langticket)")
        kategorie_wahl = input(Fore.CYAN + Style.BRIGHT + "Ihre Wahl [Nummer]: " + Style.RESET_ALL).strip()

        if kategorie_wahl in gueltige_optionen:
            play_sound("click")
            kategorie_map = {'1': 'Kurz', '2': 'Mittel', '3': 'Lang'}
            kategorie = kategorie_map[kategorie_wahl]
            print_slow(Fore.GREEN + f"✔️ {kategorie}ticket gewählt")
            break
        else:
            print_slow(
                Fore.RED + f"❌ Ungültige Eingabe '{kategorie_wahl}'. Bitte nur die Nummer eingeben: {', '.join(gueltige_optionen)}")
            play_sound("error")

    # Ticketart wählen
    print_slow(Fore.YELLOW + "\n" + "═" * 60)
    print_slow(Fore.BLUE + Style.BRIGHT + "SCHRITT 2: TICKETART WÄHLEN")
    print_slow(Fore.YELLOW + "═" * 60)
    print_slow(Fore.WHITE + "\n  [1] Einzelticket           - 1x Fahrt, 90 Min. gültig")
    print_slow(Fore.WHITE + "  [2] Mehrfahrtenticket      - 4x Fahrten, günstiger pro Fahrt")

    while True:
        print_slow(Fore.YELLOW + "\n→ Bitte geben Sie die Nummer ein (1 oder 2)")
        art_wahl = input(Fore.CYAN + Style.BRIGHT + "Ihre Wahl [Nummer]: " + Style.RESET_ALL).strip()

        if art_wahl in ['1', '2']:
            play_sound("click")
            ist_einzelticket = (art_wahl == '1')
            ticketart = 'Einzel' if ist_einzelticket else 'Mehrfahrt'
            print_slow(Fore.GREEN + f"✔️ {ticketart}ticket gewählt")
            break
        else:
            print_slow(Fore.RED + f"❌ Ungültige Eingabe '{art_wahl}'. Bitte nur '1' oder '2' eingeben.")
            play_sound("error")

    print_slow(Fore.YELLOW + "═" * 60)
    return kategorie, ticketart, ist_einzelticket


def berechne_endpreis(kategorie, ticketart, ist_einzelticket, sozialrabatt, barzahlung):
    """Berechnet den Endpreis mit allen Zuschlägen und Rabatten"""
    basispreis = TICKETPREISE[kategorie][ticketart]

    # Regelanwendung
    aufschlag_einzelticket = 10 if ist_einzelticket else 0
    rabatt_sozial = 20 if sozialrabatt else 0
    gebuehr_bar = 15 if barzahlung else 0

    # Berechnung
    aufschlag_betrag = basispreis * (aufschlag_einzelticket / 100)
    rabatt_betrag = basispreis * (rabatt_sozial / 100)
    gebuehr_betrag = basispreis * (gebuehr_bar / 100)

    endpreis = basispreis + aufschlag_betrag - rabatt_betrag + gebuehr_betrag

    return {
        'basispreis': basispreis,
        'aufschlag_einzelticket': aufschlag_einzelticket,
        'aufschlag_betrag': aufschlag_betrag,
        'rabatt_sozial': rabatt_sozial,
        'rabatt_betrag': rabatt_betrag,
        'gebuehr_bar': gebuehr_bar,
        'gebuehr_betrag': gebuehr_betrag,
        'endpreis': endpreis
    }


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

    # Zeige verfügbare Tickets
    zeige_verfuegbare_tickets(anzahl_stationen)

    # Ticketwahl
    kategorie, ticketart, ist_einzelticket = erfrage_ticketwahl(anzahl_stationen)

    basispreis = TICKETPREISE[kategorie][ticketart]
    print_slow(Fore.GREEN + f"\n✓ {kategorie}ticket ({ticketart}) gewählt")
    print_slow(Fore.CYAN + f"📋 Basispreis: €{basispreis:.2f}")

    # Rabatt- und Zuschlagsoptionen
    print_slow(Fore.BLUE + "\n--- Rabatt- & Zahlungsoptionen ---")
    print_slow(Fore.WHITE + "Bitte mit 'j' für Ja oder 'n' für Nein antworten:\n")

    sozialrabatt = erfrage_ja_nein("1. Sozialrabatt berechtigt? (-20%)")
    barzahlung = erfrage_ja_nein("2. Barzahlung? (+15% Gebühr)")

    # Preisberechnung
    preis_info = berechne_endpreis(kategorie, ticketart, ist_einzelticket, sozialrabatt, barzahlung)

    # Kaufdatum und Gültigkeitszeitraum
    jetzt = datetime.now()
    gueltig_bis = jetzt + timedelta(minutes=90) if ist_einzelticket else None

    # Quittung
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

    # Ticketdetails
    print_slow(Fore.CYAN + f"Ticketkategorie: {kategorie}ticket")
    print_slow(
        Fore.CYAN + f"Ticketart:       {ticketart}ticket" + (" (4x Einzelfahrten)" if ticketart == "Mehrfahrt" else ""))
    print_slow(Fore.CYAN + f"Basispreis:      €{preis_info['basispreis']:.2f}")

    # Aufschläge und Rabatte
    if preis_info['aufschlag_einzelticket'] > 0:
        print_slow(
            Fore.RED + f"Aufschlag Einzelticket (+{preis_info['aufschlag_einzelticket']}%): +€{preis_info['aufschlag_betrag']:.2f}")

    if preis_info['rabatt_sozial'] > 0:
        print_slow(
            Fore.GREEN + f"Sozialrabatt (-{preis_info['rabatt_sozial']}%):      -€{preis_info['rabatt_betrag']:.2f}")

    if preis_info['gebuehr_bar'] > 0:
        print_slow(
            Fore.RED + f"Gebühr Barzahlung (+{preis_info['gebuehr_bar']}%): +€{preis_info['gebuehr_betrag']:.2f}")

    print_slow(Fore.YELLOW + "—" * 60)
    print_slow(Fore.WHITE + Style.BRIGHT + f"ENDPREIS:        €{preis_info['endpreis']:.2f}")
    print_slow(Fore.YELLOW + "—" * 60)

    # Gültigkeitsinformationen
    print_slow(Fore.MAGENTA + f"\nKaufdatum: {jetzt.strftime('%d.%m.%Y %H:%M:%S')}")

    if ist_einzelticket:
        print_slow(Fore.MAGENTA + f"Gültig bis: {gueltig_bis.strftime('%d.%m.%Y %H:%M:%S')} (90 Minuten)")
        print_slow(Fore.YELLOW + "⚠️  Nur gültig für eine Fahrtrichtung")
    else:
        print_slow(Fore.MAGENTA + "Enthält: 4 Einzelfahrten (jeweils 90 Min. gültig)")
        print_slow(Fore.YELLOW + "💡 Jede Fahrt einzeln bei Fahrtantritt entwerten")

    print_slow(Fore.YELLOW + "═" * 60)

    play_sound("complete")
    print_slow(Fore.GREEN + "\n✅ Vielen Dank für Ihre Buchung! Gute Fahrt! 🚇")


if __name__ == "__main__":
    starte_fahrkarten_automat()