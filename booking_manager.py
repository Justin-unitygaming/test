import json
import os

class BookingManager:
    def __init__(self, filename='bookings.json'):
        self.filename = filename
        self.data = {"slots": []}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {"slots": []}
        else:
            self.data = {"slots": []}

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_slot(self, datetime_str, description):
        # Generate a simple ID
        if not self.data["slots"]:
            slot_id = 1
        else:
            slot_id = max(slot["id"] for slot in self.data["slots"]) + 1

        new_slot = {
            "id": slot_id,
            "datetime": datetime_str,
            "description": description,
            "booked_by": None,
            "booked_by_name": None
        }
        self.data["slots"].append(new_slot)
        self.save()
        return slot_id

    def get_available_slots(self):
        return [slot for slot in self.data["slots"] if slot["booked_by"] is None]

    def book_slot(self, slot_id, user_id, user_name):
        for slot in self.data["slots"]:
            if slot["id"] == slot_id:
                if slot["booked_by"] is not None:
                    return False, "Slot already booked."
                slot["booked_by"] = user_id
                slot["booked_by_name"] = user_name
                self.save()
                return True, "Success"
        return False, "Slot not found."

    def cancel_booking(self, slot_id, user_id):
        for slot in self.data["slots"]:
            if slot["id"] == slot_id:
                if slot["booked_by"] != user_id:
                    return False, "You didn't book this slot."
                slot["booked_by"] = None
                slot["booked_by_name"] = None
                self.save()
                return True, "Success"
        return False, "Slot not found."

    def get_user_bookings(self, user_id):
        return [slot for slot in self.data["slots"] if slot["booked_by"] == user_id]
