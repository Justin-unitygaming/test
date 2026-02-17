# Discord Buchungssystem Bot

Ein einfacher Discord-Bot für ein Buchungssystem, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen
- **Slots hinzufügen/löschen**: Administratoren können Buchungsslots erstellen und entfernen.
- **Slots anzeigen**: Nutzer können alle verfügbaren Slots einsehen.
- **Buchen**: Nutzer können einen freien Platz in einem Slot buchen.
- **Eigene Buchungen**: Nutzer können ihre aktuellen Buchungen einsehen.
- **Stornieren**: Nutzer können ihre Buchungen wieder rückgängig machen.
- **Teilnehmerliste**: Administratoren können eine Liste aller Buchungen und Teilnehmer einsehen.

## Befehle
- `/add_slot [zeit] [beschreibung] [max_teilnehmer]` (Nur Admin)
- `/delete_slot [slot_id]` (Nur Admin)
- `/list_all_slots` (Nur Admin)
- `/view_slots`
- `/book [slot_id]`
- `/my_bookings`
- `/cancel [slot_id]`

## Installation

1. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

2. Erstelle eine `.env` Datei im Hauptverzeichnis und füge deinen Discord-Bot-Token hinzu:
   ```env
   DISCORD_TOKEN=DEIN_TOKEN_HIER
   ```

3. Starte den Bot:
   ```bash
   python3 bot.py
   ```

## Tests
Du kannst die Unit-Tests für die Buchungslogik mit folgendem Befehl ausführen:
```bash
python3 test_manager.py
```
