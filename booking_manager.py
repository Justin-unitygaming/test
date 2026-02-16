import json
import os
from datetime import datetime

class BookingManager:
    def __init__(self, filename="bookings.json"):
        self.filename = filename
        self.slots = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.slots = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.slots = []
        else:
            self.slots = []

    def save_data(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.slots, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_slot(self, time_str, description, max_participants=1):
        slot_id = max([s['id'] for s in self.slots], default=0) + 1
        new_slot = {
            "id": slot_id,
            "time": time_str,
            "description": description,
            "max_participants": max_participants,
            "booked_by": []
        }
        self.slots.append(new_slot)
        self.save_data()
        return new_slot

    def delete_slot(self, slot_id):
        for i, slot in enumerate(self.slots):
            if slot["id"] == slot_id:
                deleted_slot = self.slots.pop(i)
                # Re-index remaining slots to keep IDs consistent and sequential if desired,
                # but simple pop is easier. Let's just remove it.
                self.save_data()
                return deleted_slot
        return None

    def get_slots(self):
        return self.slots

    def book_slot(self, slot_id, user_id, user_name):
        for slot in self.slots:
            if slot["id"] == slot_id:
                if len(slot["booked_by"]) >= slot["max_participants"]:
                    return False, "Dieser Slot ist bereits voll belegt."

                # Check if user already booked this slot
                for booking in slot["booked_by"]:
                    if booking["user_id"] == user_id:
                        return False, "Du hast diesen Slot bereits gebucht."

                slot["booked_by"].append({"user_id": user_id, "user_name": user_name})
                self.save_data()
                return True, "Buchung erfolgreich!"
        return False, "Slot nicht gefunden."

    def cancel_booking(self, slot_id, user_id):
        for slot in self.slots:
            if slot["id"] == slot_id:
                for i, booking in enumerate(slot["booked_by"]):
                    if booking["user_id"] == user_id:
                        slot["booked_by"].pop(i)
                        self.save_data()
                        return True, "Buchung storniert."
                return False, "Du hast diesen Slot nicht gebucht."
        return False, "Slot nicht gefunden."

    def get_user_bookings(self, user_id):
        user_bookings = []
        for slot in self.slots:
            for booking in slot["booked_by"]:
                if booking["user_id"] == user_id:
                    user_bookings.append(slot)
                    break
        return user_bookings
