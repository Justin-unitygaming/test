# Discord Buchungssystem Bot

Ein einfaches Buchungssystem für Discord, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen

- **Slots erstellen (Admin):** Erstelle Buchungs-Slots mit Datum, Uhrzeit und maximaler Teilnehmerzahl.
- **Slots ansehen:** Benutzer können alle verfügbaren Slots mit freien Plätzen einsehen.
- **Buchen:** Benutzer können einen Slot über dessen ID buchen.
- **Eigene Buchungen:** Benutzer können ihre aktiven Buchungen einsehen.
- **Stornieren:** Benutzer können ihre Buchungen stornieren.
- **Admin-Übersicht:** Admins können alle Slots und deren aktuelle Teilnehmerzahlen einsehen.
- **Slot löschen (Admin):** Admins können Slots entfernen.

## Slash Commands

- `/add_slot [datum] [uhrzeit] [max_teilnehmer]` - Fügt einen neuen Slot hinzu (Nur Admins).
- `/view_slots` - Zeigt alle verfügbaren Slots an.
- `/book [slot_id]` - Buch einen freien Slot.
- `/my_bookings` - Zeigt deine aktuellen Buchungen.
- `/cancel [slot_id]` - Storniert eine deiner Buchungen.
- `/delete_slot [slot_id]` - Löscht einen Slot (Nur Admins).
- `/list_all_slots` - Listet alle Slots mit Teilnehmerzahlen auf (Nur Admins).

## Installation

1. Klone das Repository.
2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
3. Erstelle eine `.env` Datei im Hauptverzeichnis und füge deinen Discord Bot Token hinzu:
   ```
   DISCORD_TOKEN=DEIN_TOKEN_HIER
   ```
4. Starte den Bot:
   ```bash
   python bot.py
   ```

## Tests

Um die Logik des Buchungssystems zu testen, führe die Unit-Tests aus:
```bash
python3 test_manager.py
```

## Technologien

- [Python 3.12](https://www.python.org/)
- [py-cord](https://docs.pycord.dev/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
