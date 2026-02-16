# Einfaches Discord Buchungssystem

Ein einfacher Discord Bot, um Buchungen für Events oder Termine zu verwalten. Erstellt mit der `py-cord` Bibliothek.

## Funktionen

- `/add_slot`: Neuen Buchungsslot hinzufügen (Admin).
- `/delete_slot`: Slot löschen (Admin).
- `/list_all_slots`: Alle Slots und Teilnehmer anzeigen (Admin).
- `/view_slots`: Verfügbare Slots für Benutzer anzeigen.
- `/book`: Einen Slot buchen.
- `/my_bookings`: Eigene Buchungen anzeigen.
- `/cancel`: Eine Buchung stornieren.

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

## Tests

Du kannst die Logik des Buchungsmanagers mit Unittests überprüfen:
```bash
python3 test_manager.py
```

## Datenhaltung

Die Buchungen werden in einer `bookings.json` Datei gespeichert.
