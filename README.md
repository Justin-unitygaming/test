# Discord Buchungssystem Bot

Ein einfaches Buchungssystem für Discord, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen

- **Slots verwalten (Admin):** Hinzufügen, Löschen und Auflisten aller Slots.
- **Buchen:** Benutzer können verfügbare Zeitfenster buchen.
- **Übersicht:** Benutzer können ihre eigenen Buchungen einsehen.
- **Stornieren:** Benutzer können ihre Buchungen wieder absagen.

## Befehle

### Admin-Befehle
- `/add_slot <zeit> <kapazität>`: Erstellt einen neuen Buchungsslot.
- `/delete_slot <id>`: Löscht einen existierenden Slot.
- `/list_all_slots`: Zeigt alle Slots inklusive der User-IDs an, die gebucht haben.

### Benutzer-Befehle
- `/view_slots`: Zeigt alle verfügbaren Slots an.
- `/book <id>`: Bucht einen freien Slot.
- `/my_bookings`: Zeigt die eigenen Buchungen an.
- `/cancel <id>`: Storniert eine eigene Buchung.

## Installation

1. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

2. Erstelle eine `.env` Datei im Hauptverzeichnis und füge deinen Discord Bot Token hinzu:
   ```env
   DISCORD_TOKEN=DEIN_BOT_TOKEN_HIER
   ```

3. Starte den Bot:
   ```bash
   python bot.py
   ```

## Dateien

- `bot.py`: Der Haupt-Bot-Code mit allen Slash-Commands.
- `booking_manager.py`: Logik zur Verwaltung der Buchungen und Speicherung in JSON.
- `bookings.json`: (Wird automatisch erstellt) Speichert alle Buchungsdaten permanent.
- `test_manager.py`: Unit Tests für die Buchungslogik.
