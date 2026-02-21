import json
import asyncio
import os

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.lock = asyncio.Lock()
        self.data = {"slots": [], "bookings": []}
        if os.path.exists(self.filename):
            self._load_sync()

    def _load_sync(self):
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.data = {"slots": [], "bookings": []}

    def _save_sync(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    async def add_slot(self, date, time):
        async with self.lock:
            slot_ids = [s['id'] for s in self.data['slots']]
            new_id = max(slot_ids) + 1 if slot_ids else 1
            new_slot = {
                "id": new_id,
                "date": date,
                "time": time,
                "available": True
            }
            self.data['slots'].append(new_slot)
            self._save_sync()
        return new_id

    async def delete_slot(self, slot_id):
        async with self.lock:
            self.data['slots'] = [s for s in self.data['slots'] if s['id'] != slot_id]
            self.data['bookings'] = [b for b in self.data['bookings'] if b['slot_id'] != slot_id]
            self._save_sync()

    async def get_all_slots(self):
        async with self.lock:
            return list(self.data['slots'])

    async def get_available_slots(self):
        async with self.lock:
            return [s for s in self.data['slots'] if s['available']]

    async def book_slot(self, slot_id, user_id, user_name):
        async with self.lock:
            slot = next((s for s in self.data['slots'] if s['id'] == slot_id), None)
            if not slot:
                return False, "Slot nicht gefunden."
            if not slot['available']:
                return False, "Slot ist bereits gebucht."

            slot['available'] = False
            booking = {
                "slot_id": slot_id,
                "user_id": user_id,
                "user_name": user_name,
                "date": slot['date'],
                "time": slot['time']
            }
            self.data['bookings'].append(booking)
            self._save_sync()
            return True, "Erfolgreich gebucht!"

    async def cancel_booking(self, slot_id, user_id):
        async with self.lock:
            booking_index = next((i for i, b in enumerate(self.data['bookings']) if b['slot_id'] == slot_id and b['user_id'] == user_id), None)
            if booking_index is None:
                return False, "Buchung nicht gefunden."

            self.data['bookings'].pop(booking_index)
            slot = next((s for s in self.data['slots'] if s['id'] == slot_id), None)
            if slot:
                slot['available'] = True

            self._save_sync()
            return True, "Buchung erfolgreich storniert."

    async def get_user_bookings(self, user_id):
        async with self.lock:
            return [b for b in self.data['bookings'] if b['user_id'] == user_id]
