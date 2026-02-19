import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_bookings.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = BookingManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_slot(self):
        slot_id = self.manager.add_slot("Monday 10:00", 2)
        self.assertEqual(slot_id, 1)
        self.assertEqual(len(self.manager.get_all_slots()), 1)

        slot_id_2 = self.manager.add_slot("Monday 11:00", 1)
        self.assertEqual(slot_id_2, 2)
        self.assertEqual(len(self.manager.get_all_slots()), 2)

    def test_delete_slot(self):
        slot_id = self.manager.add_slot("Monday 10:00", 2)
        success = self.manager.delete_slot(slot_id)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.get_all_slots()), 0)

        success_fail = self.manager.delete_slot(999)
        self.assertFalse(success_fail)

    def test_book_slot(self):
        slot_id = self.manager.add_slot("Monday 10:00", 2)
        user1 = 123
        user2 = 456
        user3 = 789

        # Success booking
        success, msg = self.manager.book_slot(slot_id, user1)
        self.assertTrue(success)
        self.assertIn(user1, self.manager.get_all_slots()[0]['booked_by'])

        # Already booked
        success, msg = self.manager.book_slot(slot_id, user1)
        self.assertFalse(success)
        self.assertEqual(msg, "Du hast diesen Slot bereits gebucht.")

        # Second user booking
        success, msg = self.manager.book_slot(slot_id, user2)
        self.assertTrue(success)

        # Slot full
        success, msg = self.manager.book_slot(slot_id, user3)
        self.assertFalse(success)
        self.assertEqual(msg, "Dieser Slot ist bereits voll.")

    def test_cancel_booking(self):
        slot_id = self.manager.add_slot("Monday 10:00", 2)
        user1 = 123
        self.manager.book_slot(slot_id, user1)

        # Success cancel
        success, msg = self.manager.cancel_booking(slot_id, user1)
        self.assertTrue(success)
        self.assertNotIn(user1, self.manager.get_all_slots()[0]['booked_by'])

        # Not booked
        success, msg = self.manager.cancel_booking(slot_id, user1)
        self.assertFalse(success)
        self.assertEqual(msg, "Du hast diesen Slot nicht gebucht.")

    def test_get_user_bookings(self):
        slot1 = self.manager.add_slot("Time 1", 2)
        slot2 = self.manager.add_slot("Time 2", 2)
        user1 = 123

        self.manager.book_slot(slot1, user1)
        self.manager.book_slot(slot2, user1)

        bookings = self.manager.get_user_bookings(user1)
        self.assertEqual(len(bookings), 2)
        self.assertEqual(bookings[0]['id'], slot1)
        self.assertEqual(bookings[1]['id'], slot2)

    def test_persistence(self):
        slot_id = self.manager.add_slot("Persistence Test", 5)
        self.manager.book_slot(slot_id, 123)

        # Create a new manager instance with the same file
        new_manager = BookingManager(self.test_file)
        self.assertEqual(len(new_manager.get_all_slots()), 1)
        self.assertEqual(new_manager.get_all_slots()[0]['time'], "Persistence Test")
        self.assertIn(123, new_manager.get_all_slots()[0]['booked_by'])

if __name__ == "__main__":
    unittest.main()
