import json
import os

class BookingManager:
    def __init__(self, filename="bookings.json"):
        self.filename = filename
        self.slots = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.slots, f, indent=4, ensure_ascii=False)

    def add_slot(self, time_description, max_capacity):
        slot_id = 1
        if self.slots:
            slot_id = max(slot['id'] for slot in self.slots) + 1

        new_slot = {
            "id": slot_id,
            "time": time_description,
            "max_capacity": max_capacity,
            "booked_by": []  # List of user IDs
        }
        self.slots.append(new_slot)
        self._save_data()
        return slot_id

    def delete_slot(self, slot_id):
        initial_count = len(self.slots)
        self.slots = [slot for slot in self.slots if slot['id'] != slot_id]
        if len(self.slots) < initial_count:
            self._save_data()
            return True
        return False

    def book_slot(self, slot_id, user_id):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if user_id in slot['booked_by']:
                    return False, "Du hast diesen Slot bereits gebucht."
                if len(slot['booked_by']) < slot['max_capacity']:
                    slot['booked_by'].append(user_id)
                    self._save_data()
                    return True, "Buchung erfolgreich!"
                return False, "Dieser Slot ist bereits voll."
        return False, "Slot nicht gefunden."

    def cancel_booking(self, slot_id, user_id):
        for slot in self.slots:
            if slot['id'] == slot_id:
                if user_id in slot['booked_by']:
                    slot['booked_by'].remove(user_id)
                    self._save_data()
                    return True, "Buchung storniert."
                return False, "Du hast diesen Slot nicht gebucht."
        return False, "Slot nicht gefunden."

    def get_all_slots(self):
        return self.slots

    def get_user_bookings(self, user_id):
        user_bookings = []
        for slot in self.slots:
            if user_id in slot['booked_by']:
                user_bookings.append(slot)
        return user_bookings
