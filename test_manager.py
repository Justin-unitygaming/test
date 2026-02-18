import unittest
import os
import json
from booking_manager import BookingManager

class TestBookingManager(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_bookings.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = BookingManager(filename=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_slot(self):
        slot_id = self.manager.add_slot("10:00", "Meeting")
        self.assertEqual(slot_id, 1)
        self.assertEqual(len(self.manager.get_slots()), 1)
        self.assertEqual(self.manager.get_slots()[0]['time'], "10:00")

    def test_book_slot(self):
        slot_id = self.manager.add_slot("11:00", "Workshop")
        success, message = self.manager.book_slot(slot_id, 12345, "TestUser")
        self.assertTrue(success)
        self.assertEqual(self.manager.get_slots()[0]['booked_by'], 12345)

        # Try to book again
        success, message = self.manager.book_slot(slot_id, 67890, "OtherUser")
        self.assertFalse(success)

    def test_cancel_booking(self):
        slot_id = self.manager.add_slot("12:00", "Lunch")
        self.manager.book_slot(slot_id, 12345, "TestUser")

        # Cancel with wrong user
        success, message = self.manager.cancel_booking(slot_id, 67890)
        self.assertFalse(success)

        # Cancel with right user
        success, message = self.manager.cancel_booking(slot_id, 12345)
        self.assertTrue(success)
        self.assertIsNone(self.manager.get_slots()[0]['booked_by'])

    def test_delete_slot(self):
        slot_id = self.manager.add_slot("13:00", "Gym")
        self.manager.delete_slot(slot_id)
        self.assertEqual(len(self.manager.get_slots()), 0)

    def test_id_generation(self):
        id1 = self.manager.add_slot("14:00", "A")
        id2 = self.manager.add_slot("15:00", "B")
        self.manager.delete_slot(id1)
        id3 = self.manager.add_slot("16:00", "C")
        self.assertEqual(id3, 3) # Based on max(ids) + 1

if __name__ == '__main__':
    unittest.main()
