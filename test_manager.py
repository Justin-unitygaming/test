import unittest
import os
import json
import asyncio
from booking_manager import BookingManager

class TestBookingManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.test_file = 'test_bookings.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = BookingManager(self.test_file)

    async def asyncTearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    async def test_add_slot(self):
        slot_id, error = await self.manager.add_slot("2025-10-01", "10:00", 5)
        self.assertEqual(slot_id, 1)
        self.assertIsNone(error)
        slots = await self.manager.get_slots()
        self.assertEqual(len(slots), 1)
        self.assertEqual(slots[0]['date'], "2025-10-01")

    async def test_invalid_datetime(self):
        slot_id, error = await self.manager.add_slot("invalid", "date", 5)
        self.assertIsNone(slot_id)
        self.assertIn("Ungültiges", error)

    async def test_id_generation(self):
        id1, _ = await self.manager.add_slot("2025-10-01", "10:00", 5)
        id2, _ = await self.manager.add_slot("2025-10-01", "11:00", 5)
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

        await self.manager.delete_slot(1)
        id3, _ = await self.manager.add_slot("2025-10-01", "12:00", 5)
        self.assertEqual(id3, 3) # max(2) + 1 = 3

    async def test_book_slot(self):
        slot_id, _ = await self.manager.add_slot("2025-10-01", "10:00", 1)
        success, message = await self.manager.book_slot(slot_id, "user1")
        self.assertTrue(success)

        # Double booking
        success, message = await self.manager.book_slot(slot_id, "user1")
        self.assertFalse(success)

        # Overbooking
        success, message = await self.manager.book_slot(slot_id, "user2")
        self.assertFalse(success)

    async def test_cancel_booking(self):
        slot_id, _ = await self.manager.add_slot("2025-10-01", "10:00", 5)
        await self.manager.book_slot(slot_id, "user1")

        success, message = await self.manager.cancel_booking(slot_id, "user1")
        self.assertTrue(success)

        slots = await self.manager.get_slots()
        self.assertNotIn("user1", slots[0]['participants'])

    async def test_persistence(self):
        slot_id, _ = await self.manager.add_slot("2025-10-01", "10:00", 5)
        await self.manager.book_slot(slot_id, "user1")

        # Create new manager with same file
        new_manager = BookingManager(self.test_file)
        slots = await new_manager.get_slots()
        self.assertEqual(len(slots), 1)
        self.assertIn("user1", slots[0]['participants'])

if __name__ == '__main__':
    unittest.main()
