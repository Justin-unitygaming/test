import json
import asyncio
import os
from datetime import datetime

class BookingManager:
    def __init__(self, filepath="bookings.json"):
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
        # Assumes lock is already held
        def save_sync():
            tmp_path = f"{self.filepath}.tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.slots, f, indent=4, ensure_ascii=False)
            os.replace(tmp_path, self.filepath)

        await asyncio.to_thread(save_sync)

    async def add_slot(self, datetime_str, description, capacity=1):
        # Validation
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None, "Ungültiges Datumsformat. Bitte verwende 'YYYY-MM-DD HH:MM'."

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
            return [slot for slot in self.slots if len(slot["bookings"]) < slot["capacity"]]

    async def get_user_bookings(self, user_id):
        async with self.lock:
            user_id_str = str(user_id)
            return [slot for slot in self.slots if user_id_str in [str(u) for u in slot["bookings"]]]

    async def get_all_slots(self):
        async with self.lock:
            # Return a copy to avoid external modification of the list
            return list(self.slots)

    async def get_slot_by_id(self, slot_id):
        async with self.lock:
            for slot in self.slots:
                if slot["id"] == slot_id:
                    return dict(slot)
            return None
