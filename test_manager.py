import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_bookings.json'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.manager = BookingManager(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_slot(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event")
        self.assertEqual(slot_id, 1)
        self.assertEqual(len(self.manager.data["slots"]), 1)
        self.assertEqual(self.manager.data["slots"][0]["description"], "Test Event")

    def test_get_available_slots(self):
        self.manager.add_slot("2023-12-01 10:00", "Event 1")
        self.manager.add_slot("2023-12-01 11:00", "Event 2")
        self.manager.book_slot(1, 123, "User1")

        available = self.manager.get_available_slots()
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0]["id"], 2)

    def test_book_slot(self):
        self.manager.add_slot("2023-12-01 10:00", "Event 1")
        success, message = self.manager.book_slot(1, 123, "User1")
        self.assertTrue(success)
        self.assertEqual(self.manager.data["slots"][0]["booked_by"], 123)

        # Try booking already booked slot
        success, message = self.manager.book_slot(1, 456, "User2")
        self.assertFalse(success)
        self.assertEqual(message, "Slot already booked.")

    def test_cancel_booking(self):
        self.manager.add_slot("2023-12-01 10:00", "Event 1")
        self.manager.book_slot(1, 123, "User1")

        # Wrong user tries to cancel
        success, message = self.manager.cancel_booking(1, 456)
        self.assertFalse(success)

        # Correct user cancels
        success, message = self.manager.cancel_booking(1, 123)
        self.assertTrue(success)
        self.assertIsNone(self.manager.data["slots"][0]["booked_by"])

    def test_get_user_bookings(self):
        self.manager.add_slot("2023-12-01 10:00", "Event 1")
        self.manager.add_slot("2023-12-01 11:00", "Event 2")
        self.manager.book_slot(1, 123, "User1")
        self.manager.book_slot(2, 456, "User2")

        user1_bookings = self.manager.get_user_bookings(123)
        self.assertEqual(len(user1_bookings), 1)
        self.assertEqual(user1_bookings[0]["id"], 1)

if __name__ == '__main__':
    unittest.main()
