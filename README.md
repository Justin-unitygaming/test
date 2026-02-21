# Discord Buchungssystem Bot

Ein einfacher Discord Bot für ein Buchungssystem, erstellt mit Python und der pycord Bibliothek.

## Funktionen

- **/view_slots**: Zeigt alle verfügbaren Termine an.
- **/book <slot_id>**: Buche einen verfügbaren Termin.
- **/my_bookings**: Zeigt deine aktuellen Buchungen an.
- **/cancel <slot_id>**: Storniert eine deiner Buchungen.
- **/add_slot <datum> <uhrzeit>**: Fügt einen neuen Termin hinzu (Administrator).
- **/delete_slot <slot_id>**: Löscht einen Termin (Administrator).
- **/list_all_slots**: Listet alle Termine inklusive Buchungsstatus auf (Administrator).

## Installation

1. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

2. Erstelle eine `.env` Datei im Hauptverzeichnis und füge deinen Discord Bot Token hinzu:
   ```
   DISCORD_TOKEN=DEIN_BOT_TOKEN_HIER
   ```

3. Starte den Bot:
   ```bash
   python bot.py
   ```

## Tests

Die Logik des Buchungsmanagers kann mit folgendem Befehl getestet werden:
```bash
python3 test_manager.py
```
