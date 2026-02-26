# Discord Buchungssystem Bot

Ein einfacher Discord Bot zum Verwalten von Buchungsslots, entwickelt mit Python und der `py-cord` Bibliothek.

## Funktionen

- **Slots erstellen & löschen:** Administratoren können Buchungsslots mit Datum, Beschreibung und Kapazität anlegen.
- **Slots anzeigen:** Nutzer können alle verfügbaren freien Slots einsehen.
- **Buchungssytem:** Nutzer können Slots per ID buchen und ihre eigenen Buchungen verwalten.
- **Persistenz:** Alle Daten werden in einer `bookings.json` Datei gespeichert.

## Befehle

### Für Administratoren
- `/add_slot`: Erstellt einen neuen Buchungstermin.
- `/delete_slot`: Entfernt einen vorhandenen Termin.
- `/list_all_slots`: Zeigt alle Termine inklusive Buchungsstatus an.
- `/show_bookings`: Zeigt die Nutzerdetails für einen spezifischen Slot an.

### Für Nutzer
- `/view_slots`: Zeigt alle aktuell verfügbaren Termine an.
- `/book`: Bucht einen freien Termin.
- `/my_bookings`: Zeigt die eigenen gebuchten Termine an.
- `/cancel`: Storniert eine eigene Buchung.
- `/help`: Zeigt eine Übersicht aller Befehle an.

## Einrichtung

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

Um die Logik des Buchungsmanagers zu testen, führe folgenden Befehl aus:
```bash
python3 test_manager.py
```
