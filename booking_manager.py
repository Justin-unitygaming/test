import json
import os
import uuid

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.slots = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.slots, f, indent=4)

    def add_slot(self, date, time, description):
        slot_id = str(uuid.uuid4())[:8]
        new_slot = {
            'id': slot_id,
            'date': date,
            'time': time,
            'description': description,
            'booked_by': None,
            'booked_by_name': None
        }
        self.slots.append(new_slot)
        self._save_data()
        return slot_id

    def delete_slot(self, slot_id):
        initial_count = len(self.slots)
        self.slots = [s for s in self.slots if s['id'] != slot_id]
        if len(self.slots) < initial_count:
            self._save_data()
            return True
        return False

    def get_available_slots(self):
        return [s for s in self.slots if s['booked_by'] is None]

    def get_all_slots(self):
        return self.slots

    def book_slot(self, slot_id, user_id, user_name):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if slot['booked_by'] is None:
                    slot['booked_by'] = user_id
                    slot['booked_by_name'] = user_name
                    self._save_data()
                    return True, "Slot erfolgreich gebucht."
                else:
                    return False, "Dieser Slot ist bereits gebucht."
        return False, "Slot nicht gefunden."

    def cancel_booking(self, slot_id, user_id):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if slot['booked_by'] == user_id:
                    slot['booked_by'] = None
                    slot['booked_by_name'] = None
                    self._save_data()
                    return True, "Buchung erfolgreich storniert."
                else:
                    return False, "Sie haben diesen Slot nicht gebucht."
        return False, "Slot nicht gefunden."

    def get_user_bookings(self, user_id):
        return [s for s in self.slots if s['booked_by'] == user_id]
