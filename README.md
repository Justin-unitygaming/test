# Discord Buchungssystem Bot

Ein einfacher Discord Bot zum Verwalten und Buchen von Terminslots, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen

- **Slots erstellen**: Admins können Buchungsslots mit Zeit und Beschreibung hinzufügen.
- **Slots anzeigen**: Benutzer können alle verfügbaren freien Slots sehen.
- **Buchen**: Benutzer können einen Slot über seine ID buchen.
- **Meine Buchungen**: Benutzer können ihre eigenen Buchungen einsehen.
- **Stornieren**: Benutzer können ihre eigenen Buchungen stornieren.
- **Admin-Verwaltung**: Admins können alle Buchungen einsehen und Slots löschen.

## Slash Commands

- `/add_slot <zeit> <beschreibung>`: Fügt einen neuen Slot hinzu (Admin).
- `/view_slots`: Zeigt alle freien Slots an.
- `/book <slot_id>`: Buche einen Slot.
- `/my_bookings`: Zeigt deine Buchungen an.
- `/cancel <slot_id>`: Storniert deine Buchung.
- `/delete_slot <slot_id>`: Löscht einen Slot (Admin).
- `/list_all_slots`: Zeigt alle Slots inkl. Buchungsstatus an (Admin).

## Installation

1. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

2. Erstelle eine `.env` Datei im Hauptverzeichnis und füge deinen Discord Bot Token hinzu:
   ```env
   DISCORD_TOKEN=DEIN_TOKEN_HIER
   ```

3. Starte den Bot:
   ```bash
   python bot.py
   ```

## Tests

Um die Logik des BookingManagers zu testen, führe folgenden Befehl aus:
```bash
python3 test_manager.py
```
