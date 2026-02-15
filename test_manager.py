import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_bookings.json'
        self.manager = BookingManager(filename=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_slot(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "Test Slot")
        self.assertEqual(len(self.manager.slots), 1)
        self.assertEqual(self.manager.slots[0]['id'], slot_id)
        self.assertEqual(self.manager.slots[0]['description'], "Test Slot")

    def test_delete_slot(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "To Delete")
        success = self.manager.delete_slot(slot_id)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.slots), 0)

    def test_book_slot(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "To Book")
        success, message = self.manager.book_slot(slot_id, 12345, "TestUser")
        self.assertTrue(success)
        self.assertEqual(self.manager.slots[0]['booked_by'], 12345)
        self.assertEqual(self.manager.slots[0]['booked_by_name'], "TestUser")

    def test_book_already_booked_slot(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "To Book Twice")
        self.manager.book_slot(slot_id, 12345, "User1")
        success, message = self.manager.book_slot(slot_id, 67890, "User2")
        self.assertFalse(success)
        self.assertEqual(self.manager.slots[0]['booked_by'], 12345)

    def test_cancel_booking(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "To Cancel")
        self.manager.book_slot(slot_id, 12345, "TestUser")
        success, message = self.manager.cancel_booking(slot_id, 12345)
        self.assertTrue(success)
        self.assertIsNone(self.manager.slots[0]['booked_by'])

    def test_cancel_other_user_booking(self):
        slot_id = self.manager.add_slot("2023-12-24", "10:00", "Other User")
        self.manager.book_slot(slot_id, 12345, "User1")
        success, message = self.manager.cancel_booking(slot_id, 67890)
        self.assertFalse(success)
        self.assertEqual(self.manager.slots[0]['booked_by'], 12345)

    def test_persistence(self):
        self.manager.add_slot("2023-12-24", "10:00", "Persistent Slot")
        new_manager = BookingManager(filename=self.test_db)
        self.assertEqual(len(new_manager.slots), 1)
        self.assertEqual(new_manager.slots[0]['description'], "Persistent Slot")

if __name__ == '__main__':
    unittest.main()
