print("=" * 60)
print("Willkommen beim Ring-Linien Fahrkartensystem")
print("=" * 60)
print("Ringlinie: A → B → C → D → E → F → G → H → A ...")
print("\nVerfügbare Stationen:")
print("  A: Hauptbahnhof")
print("  B: Marktplatz")
print("  C: Stadtpark")
print("  D: Universität")
print("  E: Krankenhaus")
print("  F: Industriegebiet")
print("  G: Flughafen")
print("  H: Endstation")
print()

# Startstation
while True:
    start = input("Einstieg-Haltestelle (A-H): ").upper()
    if start in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        break
    else:
        print("Ungültige Eingabe! Bitte A-H eingeben.\n")

# Zielstation
while True:
    ziel = input("Ausstieg-Haltestelle (A-H): ").upper()
    if ziel in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        break
    else:
        print("Ungültige Eingabe! Bitte A-H eingeben.\n")

# Station Dictionaries
station_nummern = {
    "A": 0, "B": 1, "C": 2, "D": 3,
    "E": 4, "F": 5, "G": 6, "H": 7
}

station_namen = {
    "A": "Hauptbahnhof", "B": "Marktplatz", "C": "Stadtpark",
    "D": "Universität", "E": "Krankenhaus", "F": "Industriegebiet",
    "G": "Flughafen", "H": "Endstation"
}

start_nummer = station_nummern[start]
ziel_nummer = station_nummern[ziel]
gesamt_stationen = len(station_namen)

# Berechne beide Wege
weg_vorwarts = (ziel_nummer - start_nummer) % gesamt_stationen
weg_ruckwarts = (start_nummer - ziel_nummer) % gesamt_stationen

# Wenn Start = Ziel
if start == ziel:

    print("\nROUTENOPTIONEN")
    print(f"Sie möchten eine vollständige Rundfahrt machen!")
    print(f"Option 1: Im Uhrzeigersinn       : {gesamt_stationen} Station(en)")
    print(f"Option 2: Gegen den Uhrzeigersinn : {gesamt_stationen} Station(en)")
    print()

    while True:
        wahl = input("Richtung? Uhrzeigersinn (U) oder Gegen den Uhrzeigersinn (G)? ").upper()
        if wahl in ["U", "G"]:
            break
        else:
            print("Ungültige Eingabe! Bitte U oder G eingeben.\n")

    distanz = gesamt_stationen
    richtung = "Im Uhrzeigersinn" if wahl == "U" else "Gegen den Uhrzeigersinn"
    route_typ = "Rundfahrt"

else:

    print("\nROUTENOPTIONEN")
    print(f"Option 1: Im Uhrzeigersinn       - {weg_vorwarts} Station(en)")
    print(f"Option 2: Gegen den Uhrzeigersinn - {weg_ruckwarts} Station(en)")
    print()

    # Präferenz
    while True:
        wahl = input("Kürzeren Weg (K) oder längeren Weg (L)? ").upper()
        if wahl in ["K", "L"]:
            break
        else:
            print("Ungültige Eingabe! Bitte K oder L eingeben.\n")

    if wahl == "K":
        if weg_vorwarts <= weg_ruckwarts:
            distanz = weg_vorwarts
            richtung = "Im Uhrzeigersinn"
        else:
            distanz = weg_ruckwarts
            richtung = "Gegen den Uhrzeigersinn"
        route_typ = "kürzeste"
    else:
        if weg_vorwarts >= weg_ruckwarts:
            distanz = weg_vorwarts
            richtung = "Im Uhrzeigersinn"
        else:
            distanz = weg_ruckwarts
            richtung = "Gegen den Uhrzeigersinn"
        route_typ = "längere"

# ======= PREISBERECHNUNG NACH ENTSCHEIDUNGSTABELLE =======

# Grundpreise
if distanz <= 3:
    grundpreis = 2.50
    ticket_typ = "Kurzstrecke"
else:
    grundpreis = 5.00
    ticket_typ = "Langstrecke"

print("\n" + "=" * 60)
print("Rabatt- & Zuschlagsoptionen")
print("=" * 60)

print("Bitte mit 'j' für Ja oder 'n' für Nein antworten:\n")

while True:
    erm_input = input("1. Ermäßigungsberechtigt? (j/n): ").lower()
    if erm_input in ['j', 'n']:
        ermaessigt = (erm_input == 'j')
        break
    print("Ungültige Eingabe! Bitte 'j' oder 'n' eingeben.\n")

while True:
    bar_input = input("2. Barzahlung? (j/n): ").lower()
    if bar_input in ['j', 'n']:
        bar = (bar_input == 'j')
        break
    print("Ungültige Eingabe! Bitte 'j' oder 'n' eingeben.\n")

while True:
    einzel_input = input("3. Einzelfahrt? (j/n): ").lower()
    if einzel_input in ['j', 'n']:
        einzelfahrt = (einzel_input == 'j')
        break
    print("Ungültige Eingabe! Bitte 'j' oder 'n' eingeben.\n")

# DEBUG: Zeige die erkannten Werte
print(f"\nErkannte Werte:")
print(f"  Ermäßigt: {'Ja' if ermaessigt else 'Nein'}")
print(f"  Bar: {'Ja' if bar else 'Nein'}")
print(f"  Einzelfahrt: {'Ja' if einzelfahrt else 'Nein'}")

# ======= ENTSCHEIDUNGSTABELLE - EXAKT WIE IN DER AUFGABE =======
# Die Zuschläge sind FESTE WERTE aus der Tabelle, nicht addiert!

# Bestimme Rabatt und Zuschlag nach Entscheidungstabelle
if ermaessigt and not bar and not einzelfahrt:
    # Fall 1
    rabatt_prozent = 20
    zuschlag_prozent = 0
    aktion = "Rabatt anwenden"
elif ermaessigt and bar and not einzelfahrt:
    # Fall 2
    rabatt_prozent = 20
    zuschlag_prozent = 10
    aktion = "Rabatt + Zuschlag Bar"
elif ermaessigt and not bar and einzelfahrt:
    # Fall 3
    rabatt_prozent = 20
    zuschlag_prozent = 5
    aktion = "Rabatt + Zuschlag Einzelfahrt"
elif ermaessigt and bar and einzelfahrt:
    # Fall 4
    rabatt_prozent = 20
    zuschlag_prozent = 15
    aktion = "Rabatt + beide Zuschläge"
elif not ermaessigt and not bar and not einzelfahrt:
    # Fall 5
    rabatt_prozent = 0
    zuschlag_prozent = 0
    aktion = "Keine Anpassung"
elif not ermaessigt and bar and not einzelfahrt:
    # Fall 6
    rabatt_prozent = 0
    zuschlag_prozent = 10
    aktion = "Zuschlag Bar"
elif not ermaessigt and not bar and einzelfahrt:
    # Fall 7
    rabatt_prozent = 0
    zuschlag_prozent = 5
    aktion = "Zuschlag Einzelfahrt"
else:  # not ermaessigt and bar and einzelfahrt
    # Fall 8
    rabatt_prozent = 0
    zuschlag_prozent = 15
    aktion = "Beide Zuschläge"

# BERECHNUNG OPTION B: Rabatt und Zuschlag beide auf Grundpreis
rabatt_betrag = grundpreis * (rabatt_prozent / 100)
zuschlag_betrag = grundpreis * (zuschlag_prozent / 100)
endpreis = grundpreis - rabatt_betrag + zuschlag_betrag

# ====== AUSGABE ======
print("\n" + "=" * 60)
print("FAHRSCHEIN - RINGLINIE")
print("=" * 60)

print(f"Von:      {start} - {station_namen[start]}")
print(f"Nach:     {ziel} - {station_namen[ziel]}")
print(f"Distanz:  {distanz} Station(en) ({route_typ} Route)")

if distanz > 0:
    print(f"Richtung: {richtung}")

print(f"\n{'Ticket:':<20} {ticket_typ}")
print(f"{'Grundpreis:':<20} €{grundpreis:.2f}")

# Detaillierte Preisaufschlüsselung
if rabatt_prozent > 0:
    print(f"{'Rabatt (' + str(rabatt_prozent) + '%):':<20} -€{rabatt_betrag:.2f}")

if zuschlag_prozent > 0:
    print(f"{'Zuschlag (' + str(zuschlag_prozent) + '%):':<20} +€{zuschlag_betrag:.2f}")

print("-" * 60)
print(f"{'ENDPREIS:':<20} €{endpreis:.2f}")
print(f"{'Aktion:':<20} {aktion}")
print("=" * 60)

# Zeige Entscheidungstabelle zur Verifizierung
print("\n" + "=" * 60)
print("VERWENDETE ENTSCHEIDUNGSTABELLE")
print("=" * 60)
print(f"{'Nr.':<5} {'Ermäßigt':<12} {'Bar':<8} {'Einzelf.':<12} {'Rabatt':<10} {'Zuschlag':<12} {'Aktion':<30}")
print("-" * 60)

# Zeige alle Fälle und markiere den aktuellen
alle_faelle = [
    (1, True, False, False, 20, 0, "Rabatt anwenden"),
    (2, True, True, False, 20, 10, "Rabatt + Zuschlag Bar"),
    (3, True, False, True, 20, 5, "Rabatt + Zuschlag Einzelfahrt"),
    (4, True, True, True, 20, 15, "Rabatt + beide Zuschläge"),
    (5, False, False, False, 0, 0, "Keine Anpassung"),
    (6, False, True, False, 0, 10, "Zuschlag Bar"),
    (7, False, False, True, 0, 5, "Zuschlag Einzelfahrt"),
    (8, False, True, True, 0, 15, "Beide Zuschläge"),
]

for nr, erm, b, einz, rab, zus, akt in alle_faelle:
    marker = "→ " if (erm == ermaessigt and b == bar and einz == einzelfahrt) else "  "
    erm_str = "Ja" if erm else "Nein"
    b_str = "Ja" if b else "Nein"
    einz_str = "Ja" if einz else "Nein"
    print(f"{marker}{nr:<4} {erm_str:<12} {b_str:<8} {einz_str:<12} {rab}%{'':<7} {zus}%{'':<9} {akt:<30}")

print("=" * 60)