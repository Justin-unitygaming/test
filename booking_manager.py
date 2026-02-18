import json
import os

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.slots = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.slots, f, indent=4, ensure_ascii=False)

    def add_slot(self, time, description):
        slot_id = 1
        if self.slots:
            slot_id = max(slot['id'] for slot in self.slots) + 1

        new_slot = {
            'id': slot_id,
            'time': time,
            'description': description,
            'booked_by': None,
            'user_name': None
        }
        self.slots.append(new_slot)
        self._save_data()
        return slot_id

    def delete_slot(self, slot_id):
        self.slots = [slot for slot in self.slots if slot['id'] != slot_id]
        self._save_data()

    def book_slot(self, slot_id, user_id, user_name):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if slot['booked_by'] is not None:
                    return False, "Slot bereits gebucht."
                slot['booked_by'] = user_id
                slot['user_name'] = user_name
                self._save_data()
                return True, "Erfolgreich gebucht."
        return False, "Slot nicht gefunden."

    def cancel_booking(self, slot_id, user_id):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if slot['booked_by'] != user_id:
                    return False, "Du hast diesen Slot nicht gebucht."
                slot['booked_by'] = None
                slot['user_name'] = None
                self._save_data()
                return True, "Buchung storniert."
        return False, "Slot nicht gefunden."

    def get_slots(self):
        return self.slots

    def get_user_bookings(self, user_id):
        return [slot for slot in self.slots if slot['booked_by'] == user_id]
