import sys
import time
import os
import winsound
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# WICHTIG: init mit convert=True behebt die [36m Fehler in der Windows Konsole
init(autoreset=True, convert=True)

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ==========================================
# KLASSE: SoundManager (Multimedia-Feedback)
# ==========================================
class SoundManager:
    @staticmethod
    def play(sound_type):
        try:
            sounds = {
                "startup": [(392, 150), (523, 150), (659, 150), (784, 250)],
                "success": [(523, 150), (659, 150), (784, 200)],
                "complete": [(523, 150), (659, 150), (784, 150), (1047, 400)],
                "click": [(800, 80)]
            }
            if sound_type == "error":
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            elif sound_type in sounds:
                for freq, dur in sounds[sound_type]:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
        except:
            pass

# ==========================================
# KLASSE: Verkehrsnetz (Daten & Navigation)
# ==========================================
class Verkehrsnetz:
    def __init__(self):
        self.netz_daten = {
            "Fürth Hbf.": ["Jakobinenstr."], "Jakobinenstr.": ["Fürth Hbf.", "Stadtgrenze"],
            "Stadtgrenze": ["Jakobinenstr.", "Muggenhof"], "Muggenhof": ["Stadtgrenze", "EberhardsHof"],
            "EberhardsHof": ["Muggenhof", "Maximilianstr."], "Maximilianstr.": ["EberhardsHof", "Bärenschanze"],
            "Bärenschanze": ["Maximilianstr.", "Gostenhof"], "Gostenhof": ["Bärenschanze", "Plärrer"],
            "Gustav-Adolf-Str.": ["Sündersbühl"], "Sündersbühl": ["Gustav-Adolf-Str.", "Rothenburger Str."],
            "Plärrer": ["Rothenburger Str.", "Gostenhof", "Weißer Turm", "Opernhaus"],
            "Rothenburger Str.": ["Sündersbühl", "Plärrer", "St. Leonhard"],
            "Weißer Turm": ["Plärrer", "Lorenzkirche"], "Lorenzkirche": ["Weißer Turm", "Hauptbahnhof"],
            "Opernhaus": ["Plärrer", "Hauptbahnhof"], "Hauptbahnhof": ["Lorenzkirche", "Opernhaus", "Aufseßplatz", "Wöhrder Wiese"],
            "St. Leonhard": ["Rothenburger Str.", "Schweinau"], "Schweinau": ["St. Leonhard", "Hohe Marter"],
            "Hohe Marter": ["Schweinau", "Röthenbach"], "Röthenbach": ["Hohe Marter"],
            "Wöhrder Wiese": ["Hauptbahnhof", "Rathenauplatz"], "Rathenauplatz": ["Wöhrder Wiese", "Rennweg", "Maxfeld"],
            "Rennweg": ["Rathenauplatz", "Schoppershof"], "Schoppershof": ["Rennweg", "Nordostbahnhof"],
            "Nordostbahnhof": ["Schoppershof", "Herrnhütte"], "Herrnhütte": ["Nordostbahnhof", "Ziegelstein"],
            "Ziegelstein": ["Herrnhütte", "Flughafen"], "Flughafen": ["Ziegelstein"],
            "Aufseßplatz": ["Hauptbahnhof", "Maffeiplatz"], "Maffeiplatz": ["Aufseßplatz", "Frankenstr."],
            "Frankenstr.": ["Maffeiplatz", "Hasenbuck"], "Hasenbuck": ["Frankenstr.", "Bauernfeindstr."],
            "Bauernfeindstr.": ["Hasenbuck", "Messe"], "Messe": ["Bauernfeindstr.", "Langwasser Nord"],
            "Langwasser Nord": ["Messe", "Scharfreiterring"], "Scharfreiterring": ["Langwasser Nord", "Langwasser Mitte"],
            "Langwasser Mitte": ["Scharfreiterring", "Gemeinschaftshaus"],
            "Gemeinschaftshaus": ["Langwasser Mitte", "Langwasser Süd"], "Langwasser Süd": ["Gemeinschaftshaus"],
            "Fr.-Ebert-Platz": ["Kaulbachplatz"], "Kaulbachplatz": ["Fr.-Ebert-Platz", "Maxfeld"],
            "Maxfeld": ["Kaulbachplatz", "Rathenauplatz"],
        }
        self.linien = {
            "U1": ["Fürth Hbf.", "Jakobinenstr.", "Stadtgrenze", "Muggenhof", "EberhardsHof", "Maximilianstr.", "Bärenschanze", "Gostenhof", "Plärrer", "Weißer Turm", "Lorenzkirche", "Hauptbahnhof", "Aufseßplatz", "Maffeiplatz", "Frankenstr.", "Hasenbuck", "Bauernfeindstr.", "Messe", "Langwasser Nord", "Scharfreiterring", "Langwasser Mitte", "Gemeinschaftshaus", "Langwasser Süd"],
            "U2": ["Flughafen", "Ziegelstein", "Herrnhütte", "Nordostbahnhof", "Schoppershof", "Rennweg", "Rathenauplatz", "Wöhrder Wiese", "Hauptbahnhof", "Opernhaus", "Plärrer", "Rothenburger Str.", "St. Leonhard", "Schweinau", "Hohe Marter", "Röthenbach"],
            "U3": ["Gustav-Adolf-Str.", "Sündersbühl", "Rothenburger Str.", "Plärrer", "Weißer Turm", "Lorenzkirche", "Hauptbahnhof", "Opernhaus", "Wöhrder Wiese", "Rathenauplatz", "Maxfeld", "Kaulbachplatz", "Fr.-Ebert-Platz"]
        }
        self.stationen_liste = self._generiere_eindeutige_liste()

    def _generiere_eindeutige_liste(self):
        alle = []
        gesehen = set()
        for linie in self.linien.values():
            for s in linie:
                if s not in gesehen and s in self.netz_daten:
                    alle.append(s)
                    gesehen.add(s)
        return alle

    def finde_kuerzesten_pfad(self, start, ziel):
        warteschlange = [(start, [start])]
        besucht = {start}
        while warteschlange:
            (akt, pfad) = warteschlange.pop(0)
            for nachbar in self.netz_daten.get(akt, []):
                if nachbar == ziel: return pfad + [ziel]
                if nachbar not in besucht:
                    besucht.add(nachbar)
                    warteschlange.append((nachbar, pfad + [nachbar]))
        return None

# ==========================================
# KLASSE: Ticket (Preislogik & Berechnung)
# ==========================================
class Ticket:
    PREISE = {
        'Kurz': {'Einzel': 1.50, 'Mehrfahrt': 5.00},
        'Mittel': {'Einzel': 2.00, 'Mehrfahrt': 7.00},
        'Lang': {'Einzel': 3.00, 'Mehrfahrt': 10.00}
    }

    def __init__(self, distanz, art):
        self.distanz = distanz
        self.kategorie = self._bestimme_kategorie()
        self.art = art  # 'Einzel' oder 'Mehrfahrt'
        self.basispreis = self.PREISE[self.kategorie][self.art]

    def _bestimme_kategorie(self):
        if self.distanz <= 3: return 'Kurz'
        if self.distanz <= 8: return 'Mittel'
        return 'Lang'

    def berechne_endpreis(self, sozialrabatt, barzahlung):
        preis = self.basispreis
        if self.art == 'Einzel': preis += self.basispreis * 0.10
        if sozialrabatt: preis -= self.basispreis * 0.20
        if barzahlung: preis += self.basispreis * 0.15
        return round(preis, 2)

# ==========================================
# KLASSE: FahrkartenAutomat (Benutzer-Interface)
# ==========================================
class FahrkartenAutomat:
    def __init__(self):
        self.netz = Verkehrsnetz()
        self.sound = SoundManager()

    def print_slow(self, text, color=Fore.WHITE):
        for char in (color + text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        print(Style.RESET_ALL)

    def zeige_willkommen(self):
        self.sound.play("startup")
        print(Fore.YELLOW + "═" * 60)
        self.print_slow("🚆 WILLKOMMEN AM INTELLIGENTEN FAHRKARTENAUTOMATEN", Fore.GREEN + Style.BRIGHT)
        print(Fore.YELLOW + "═" * 60)

    def zeige_stationen(self):
        self.print_