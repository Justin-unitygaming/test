# Discord Buchungssystem Bot

Ein einfacher Discord-Bot, um Buchungsslots zu verwalten und zu buchen. Erstellt mit der `py-cord` Bibliothek.

## Funktionen

### Benutzer-Befehle
- `/view_slots`: Zeigt alle verfügbaren Buchungsslots an.
- `/book [slot_id]`: Buche einen verfügbaren Slot.
- `/my_bookings`: Zeigt deine aktuellen Buchungen an.
- `/cancel [slot_id]`: Storniere eine deiner Buchungen.

### Administrator-Befehle
- `/add_slot [datum] [zeit] [beschreibung]`: Fügt einen neuen Buchungsslot hinzu.
- `/delete_slot [slot_id]`: Entfernt einen Buchungsslot.
- `/list_all_slots`: Listet alle Slots (verfügbar und gebucht) mit Details auf.

## Einrichtung

1. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
2. Setzen Sie Ihre Discord-Bot-Token als Umgebungsvariable:
   ```bash
   export DISCORD_TOKEN='IHR_TOKEN'
   ```
3. Starten Sie den Bot:
   ```bash
   python bot.py
   ```

## Dateien
- `bot.py`: Das Haupt-Skript des Bots.
- `booking_manager.py`: Verwaltet die Buchungslogik und Persistenz.
- `bookings.json`: Speichert die Buchungsdaten.
- `test_manager.py`: Unit-Tests für die Buchungslogik.
