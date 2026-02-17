import json
import os

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.slots = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert keys to integers
                    self.slots = {int(k): v for k, v in data.get('slots', {}).items()}
            except (json.JSONDecodeError, ValueError):
                self.slots = {}
        else:
            self.slots = {}

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump({'slots': self.slots}, f, indent=4, ensure_ascii=False)

    def add_slot(self, time, description, max_participants):
        slot_id = max(self.slots.keys(), default=0) + 1
        self.slots[slot_id] = {
            'time': time,
            'description': description,
            'max_participants': max_participants,
            'participants': {} # user_id (str): username
        }
        self.save()
        return slot_id

    def delete_slot(self, slot_id):
        if slot_id in self.slots:
            del self.slots[slot_id]
            self.save()
            return True
        return False

    def list_all_slots(self):
        return self.slots

    def book(self, slot_id, user_id, user_name):
        user_id = str(user_id)
        if slot_id not in self.slots:
            return False, "Slot existiert nicht."

        slot = self.slots[slot_id]
        if user_id in slot['participants']:
            return False, "Du hast diesen Slot bereits gebucht."

        if len(slot['participants']) >= slot['max_participants']:
            return False, "Dieser Slot ist bereits voll."

        slot['participants'][user_id] = user_name
        self.save()
        return True, "Buchung erfolgreich!"

    def cancel_booking(self, slot_id, user_id):
        user_id = str(user_id)
        if slot_id not in self.slots:
            return False, "Slot existiert nicht."

        slot = self.slots[slot_id]
        if user_id not in slot['participants']:
            return False, "Du hast diesen Slot nicht gebucht."

        del slot['participants'][user_id]
        self.save()
        return True, "Buchung storniert."

    def get_my_bookings(self, user_id):
        user_id = str(user_id)
        my_bookings = []
        for slot_id, slot in self.slots.items():
            if user_id in slot['participants']:
                my_bookings.append((slot_id, slot))
        return my_bookings
