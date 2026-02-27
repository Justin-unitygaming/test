import json
import asyncio
import os

class BookingManager:
    """Verwaltet die Buchungsslots und deren Persistenz in einer JSON-Datei."""

    def __init__(self, filepath="bookings.json"):
        """Initialisiert den BookingManager und lädt vorhandene Daten."""
        self.filepath = filepath
        self.lock = asyncio.Lock()
        self.slots = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.slots = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.slots = []

    async def _save(self):
        """Speichert die aktuellen Slots atomar in der JSON-Datei."""
        # Verwendet eine temporäre Datei für atomares Schreiben
        temp_file = f"{self.filepath}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.slots, f, indent=4, ensure_ascii=False)
            os.replace(temp_file, self.filepath)
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise e

    async def add_slot(self, datetime_str, description, capacity=1):
        """Erstellt einen neuen Buchungsslot."""
        if capacity < 1:
            raise ValueError("Kapazität muss mindestens 1 sein.")

        async with self.lock:
            new_id = 1
            if self.slots:
                new_id = max(slot["id"] for slot in self.slots) + 1

            new_slot = {
                "id": new_id,
                "datetime": datetime_str,
                "description": description,
                "capacity": capacity,
                "bookings": []
            }
            self.slots.append(new_slot)
            await self._save()
            return new_id

    async def delete_slot(self, slot_id):
        """Löscht einen Slot anhand seiner ID."""
        async with self.lock:
            original_len = len(self.slots)
            self.slots = [slot for slot in self.slots if slot["id"] != slot_id]
            success = len(self.slots) < original_len
            if success:
                await self._save()
            return success

    async def book_slot(self, slot_id, user_id):
        """Bucht einen Slot für einen Nutzer."""
        async with self.lock:
            for slot in self.slots:
                if slot["id"] == slot_id:
                    if len(slot["bookings"]) >= slot["capacity"]:
                        return False, "Dieser Slot ist bereits voll belegt."

                    user_id_str = str(user_id)
                    if user_id_str in [str(u) for u in slot["bookings"]]:
                        return False, "Du hast diesen Slot bereits gebucht."

                    slot["bookings"].append(user_id_str)
                    await self._save()
                    return True, "Buchung erfolgreich!"
            return False, "Slot wurde nicht gefunden."

    async def cancel_booking(self, slot_id, user_id):
        """Storniert eine Buchung eines Nutzers."""
        async with self.lock:
            for slot in self.slots:
                if slot["id"] == slot_id:
                    user_id_str = str(user_id)
                    if user_id_str in [str(u) for u in slot["bookings"]]:
                        slot["bookings"].remove(user_id_str)
                        await self._save()
                        return True, "Buchung erfolgreich storniert."
                    return False, "Du hast diesen Slot nicht gebucht."
            return False, "Slot wurde nicht gefunden."

    async def get_available_slots(self):
        """Gibt alle noch nicht voll belegten Slots zurück."""
        async with self.lock:
            return [slot for slot in self.slots if len(slot["bookings"]) < slot["capacity"]]

    async def get_user_bookings(self, user_id):
        """Gibt alle Buchungen eines bestimmten Nutzers zurück."""
        async with self.lock:
            user_id_str = str(user_id)
            return [slot for slot in self.slots if user_id_str in [str(u) for u in slot["bookings"]]]

    async def get_all_slots(self):
        """Gibt eine Liste aller Slots zurück."""
        async with self.lock:
            # Kopie zurückgeben, um externe Modifikationen der Liste zu vermeiden
            return list(self.slots)

    async def get_slot_by_id(self, slot_id):
        """Sucht einen Slot anhand seiner ID."""
        async with self.lock:
            for slot in self.slots:
                if slot["id"] == slot_id:
                    return dict(slot)
            return None
