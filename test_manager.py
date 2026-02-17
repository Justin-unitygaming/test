import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_bookings.json'
        # Sicherstellen, dass die Test-Datenbankdatei nicht existiert
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.manager = BookingManager(self.test_db)

    def tearDown(self):
        # Nach den Tests aufräumen
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_slot(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 2)
        self.assertEqual(slot_id, 1)
        self.assertIn(1, self.manager.slots)
        self.assertEqual(self.manager.slots[1]['description'], "Test Event")

    def test_book_slot_success(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 1)
        success, msg = self.manager.book(slot_id, "user123", "Max Mustermann")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.slots[slot_id]['participants']), 1)
        self.assertEqual(self.manager.slots[slot_id]['participants']["user123"], "Max Mustermann")

    def test_book_slot_already_booked(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 2)
        self.manager.book(slot_id, "user123", "Max Mustermann")
        success, msg = self.manager.book(slot_id, "user123", "Max Mustermann")
        self.assertFalse(success)
        self.assertEqual(msg, "Du hast diesen Slot bereits gebucht.")

    def test_book_slot_full(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 1)
        self.manager.book(slot_id, "user1", "User 1")
        success, msg = self.manager.book(slot_id, "user2", "User 2")
        self.assertFalse(success)
        self.assertEqual(msg, "Dieser Slot ist bereits voll.")

    def test_cancel_booking(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 2)
        self.manager.book(slot_id, "user123", "Max Mustermann")
        success, msg = self.manager.cancel_booking(slot_id, "user123")
        self.assertTrue(success)
        self.assertEqual(len(self.manager.slots[slot_id]['participants']), 0)

    def test_delete_slot(self):
        slot_id = self.manager.add_slot("2023-12-01 10:00", "Test Event", 2)
        success = self.manager.delete_slot(slot_id)
        self.assertTrue(success)
        self.assertNotIn(slot_id, self.manager.slots)

    def test_get_my_bookings(self):
        slot_id1 = self.manager.add_slot("2023-12-01 10:00", "Event 1", 2)
        slot_id2 = self.manager.add_slot("2023-12-01 11:00", "Event 2", 2)
        self.manager.book(slot_id1, "user123", "Max")
        self.manager.book(slot_id2, "user123", "Max")

        my_bookings = self.manager.get_my_bookings("user123")
        self.assertEqual(len(my_bookings), 2)
        ids = [b[0] for b in my_bookings]
        self.assertIn(slot_id1, ids)
        self.assertIn(slot_id2, ids)

if __name__ == '__main__':
    unittest.main()
