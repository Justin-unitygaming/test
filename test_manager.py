import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_bookings.json"
        self.manager = BookingManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_slot(self):
        slot = self.manager.add_slot("2023-12-01 10:00", "Test Event", 2)
        self.assertEqual(len(self.manager.get_slots()), 1)
        self.assertEqual(slot["description"], "Test Event")

    def test_book_slot(self):
        self.manager.add_slot("2023-12-01 10:00", "Test Event", 1)
        success, message = self.manager.book_slot(1, 123, "User1")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_slots()[0]["booked_by"]), 1)

        # Try to book same slot again (full)
        success, message = self.manager.book_slot(1, 456, "User2")
        self.assertFalse(success)
        self.assertEqual(message, "Dieser Slot ist bereits voll belegt.")

    def test_cancel_booking(self):
        self.manager.add_slot("2023-12-01 10:00", "Test Event", 1)
        self.manager.book_slot(1, 123, "User1")
        success, message = self.manager.cancel_booking(1, 123)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_slots()[0]["booked_by"]), 0)

    def test_get_user_bookings(self):
        self.manager.add_slot("2023-12-01 10:00", "Event 1", 1)
        self.manager.add_slot("2023-12-01 11:00", "Event 2", 1)
        self.manager.book_slot(1, 123, "User1")
        self.manager.book_slot(2, 456, "User2")

        user1_bookings = self.manager.get_user_bookings(123)
        self.assertEqual(len(user1_bookings), 1)
        self.assertEqual(user1_bookings[0]["description"], "Event 1")

    def test_id_generation_after_deletion(self):
        # Add two slots
        self.manager.add_slot("2023-12-01 10:00", "Event 1")
        self.manager.add_slot("2023-12-01 11:00", "Event 2")

        # Delete first slot
        self.manager.delete_slot(1)

        # Add new slot - should have ID 3, not 2
        new_slot = self.manager.add_slot("2023-12-01 12:00", "Event 3")
        self.assertEqual(new_slot["id"], 3)

        # Ensure ID 2 still exists
        slots = self.manager.get_slots()
        self.assertEqual(len(slots), 2)
        ids = [s["id"] for s in slots]
        self.assertIn(2, ids)
        self.assertIn(3, ids)

if __name__ == "__main__":
    unittest.main()
