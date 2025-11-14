STATIONEN = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Preistabelle: (ermäßigt, bar, einzelfahrt) -> (rabatt%, zuschlag%)
PREISE = {
    (True, False, False): (20, 0), (True, True, False): (20, 10),
    (True, False, True): (20, 5), (True, True, True): (20, 15),
    (False, False, False): (0, 0), (False, True, False): (0, 10),
    (False, False, True): (0, 5), (False, True, True): (0, 15),
}

print("=" * 40)
print("Ring-Linien Ticket")
print("=" * 40)
print("Preise: Kurz (≤3) €2.50 | Lang (>3) €5.00")
print("Stationen: A-B-C-D-E-F-G-H-A")
print()

# Eingaben
start = input("Start (A-H): ").upper()
ziel = input("Ziel (A-H): ").upper()

# Distanz
vor = (STATIONEN.index(ziel) - STATIONEN.index(start)) % 8
zurück = 8 - vor
kurz = min(vor, zurück)
lang = max(vor, zurück)

print(f"\nKurz: {kurz} | Lang: {lang}")
weg = input("Kurz (K) oder Lang (L)? ").upper()
distanz = kurz if weg == "K" else lang

# Optionen
erm = input("Ermäßigt (j/n)? ").lower() == "j"
bar = input("Bar (j/n)? ").lower() == "j"
einzel = input("Einzelfahrt (j/n)? ").lower() == "j"

# Preis
grund = 2.50 if distanz <= 3 else 5.00
rabatt_p, zuschlag_p = PREISE[(erm, bar, einzel)]
preis = grund * (1 - rabatt_p/100 + zuschlag_p/100)

# Ausgabe
print("\n" + "=" * 40)
print(f"{start} → {ziel} ({distanz} Stationen)")
print(f"Preis: €{preis:.2f}")
print("=" * 40)