import json
import os
import asyncio
from datetime import datetime

class BookingManager:
    def __init__(self, storage_file='bookings.json'):
        self.storage_file = storage_file
        self.lock = asyncio.Lock()
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"slots": []}
        return {"slots": []}

    def _save_data(self):
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _validate_datetime(self, date_str, time_str):
        try:
            datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    async def add_slot(self, date, time, max_participants):
        if not self._validate_datetime(date, time):
            return None, "Ungültiges Datums- oder Zeitformat (Erwartet: YYYY-MM-DD HH:MM)."

        async with self.lock:
            ids = [slot['id'] for slot in self.data['slots']]
            new_id = max(ids) + 1 if ids else 1

            new_slot = {
                "id": new_id,
                "date": date,
                "time": time,
                "max_participants": max_participants,
                "participants": []
            }
            self.data['slots'].append(new_slot)
            self._save_data()
            return new_id, None

    async def delete_slot(self, slot_id):
        async with self.lock:
            initial_count = len(self.data['slots'])
            self.data['slots'] = [slot for slot in self.data['slots'] if slot['id'] != slot_id]
            if len(self.data['slots']) < initial_count:
                self._save_data()
                return True
            return False

    async def get_slots(self):
        async with self.lock:
            return list(self.data['slots'])

    async def book_slot(self, slot_id, user_id):
        async with self.lock:
            for slot in self.data['slots']:
                if slot['id'] == slot_id:
                    if user_id in slot['participants']:
                        return False, "Du hast diesen Slot bereits gebucht."
                    if len(slot['participants']) >= slot['max_participants']:
                        return False, "Dieser Slot ist bereits voll."
                    slot['participants'].append(user_id)
                    self._save_data()
                    return True, "Buchung erfolgreich."
            return False, "Slot nicht gefunden."

    async def cancel_booking(self, slot_id, user_id):
        async with self.lock:
            for slot in self.data['slots']:
                if slot['id'] == slot_id:
                    if user_id in slot['participants']:
                        slot['participants'].remove(user_id)
                        self._save_data()
                        return True, "Buchung erfolgreich storniert."
                    return False, "Du hast diesen Slot nicht gebucht."
            return False, "Slot nicht gefunden."

    async def get_user_bookings(self, user_id):
        async with self.lock:
            user_bookings = []
            for slot in self.data['slots']:
                if user_id in slot['participants']:
                    user_bookings.append(slot)
            return user_bookings
