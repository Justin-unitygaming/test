# Discord Buchungssystem Bot

Ein einfaches Buchungssystem für Discord, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen

- `/add_slot [datum/zeit] [beschreibung]`: Neuen Buchungsslot hinzufügen (Nur für Administratoren).
- `/view_slots`: Alle verfügbaren Buchungsslots anzeigen.
- `/book [slot_id]`: Einen Slot buchen.
- `/my_bookings`: Eigene Buchungen anzeigen.
- `/cancel [slot_id]`: Eine eigene Buchung stornieren.

## Voraussetzungen

- Python 3.8 oder höher
- `py-cord` Bibliothek

## Installation

1. Installiere die benötigte Bibliothek:
   ```bash
   pip install py-cord
   ```

2. Setze deinen Discord Bot Token als Umgebungsvariable:
   ```bash
   export DISCORD_TOKEN="DEIN_BOT_TOKEN"
   ```
   (Unter Windows: `set DISCORD_TOKEN=DEIN_BOT_TOKEN`)

## Starten des Bots

Führe den Bot mit folgendem Befehl aus:
```bash
python bot.py
```

## Dateien

- `bot.py`: Der Hauptcode für den Discord Bot.
- `booking_manager.py`: Logik für die Verwaltung der Buchungen und Speicherung in `bookings.json`.
- `bookings.json`: (Wird automatisch erstellt) Speichert die Buchungsdaten.
- `test_manager.py`: Unit Tests für die Buchungslogik.
