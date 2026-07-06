import json
import asyncio
import os
import copy
from datetime import datetime

class BookingManager:
    def __init__(self, filepath="bookings.json"):
        self.filepath = filepath
        self.lock = asyncio.Lock()
        self.slots = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    self.slots = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.slots = []

    def _save_sync(self):
        temp_filepath = self.filepath + ".tmp"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(self.slots, f, indent=4, ensure_ascii=False)
        os.replace(temp_filepath, self.filepath)

    async def _save(self):
        # Assumes lock is already held
        await asyncio.to_thread(self._save_sync)

    async def add_slot(self, datetime_str, description, capacity=1):
        # Validierung
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None, "Ungültiges Datumsformat. Bitte verwende YYYY-MM-DD HH:MM."

        if capacity < 1:
            return None, "Die Kapazität muss mindestens 1 sein."

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
            return new_id, None

    async def delete_slot(self, slot_id):
        async with self.lock:
            original_len = len(self.slots)
            self.slots = [slot for slot in self.slots if slot["id"] != slot_id]
            success = len(self.slots) < original_len
            if success:
                await self._save()
            return success

    async def book_slot(self, slot_id, user_id):
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
        async with self.lock:
            available = [slot for slot in self.slots if len(slot["bookings"]) < slot["capacity"]]
            return copy.deepcopy(available)

    async def get_user_bookings(self, user_id):
        async with self.lock:
            user_id_str = str(user_id)
            user_slots = [slot for slot in self.slots if user_id_str in [str(u) for u in slot["bookings"]]]
            return copy.deepcopy(user_slots)

    async def get_all_slots(self):
        async with self.lock:
            return copy.deepcopy(self.slots)

    async def get_slot_by_id(self, slot_id):
        async with self.lock:
            for slot in self.slots:
                if slot["id"] == slot_id:
                    return copy.deepcopy(slot)
            return None
