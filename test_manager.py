import unittest
import os
import json
import asyncio
from booking_manager import BookingManager

class TestBookingManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.test_file = "test_bookings.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.manager = BookingManager(self.test_file)

    async def asyncTearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    async def test_add_slot_success(self):
        slot_id, error = await self.manager.add_slot("2023-12-01 10:00", "Test Slot", 2)
        self.assertEqual(slot_id, 1)
        self.assertIsNone(error)
        slots = await self.manager.get_all_slots()
        self.assertEqual(len(slots), 1)
        self.assertEqual(slots[0]["description"], "Test Slot")
        self.assertEqual(slots[0]["capacity"], 2)

    async def test_add_slot_invalid_date(self):
        slot_id, error = await self.manager.add_slot("01-12-2023 10:00", "Invalid Date", 1)
        self.assertIsNone(slot_id)
        self.assertIn("Ungültiges Datumsformat", error)

    async def test_add_slot_invalid_capacity(self):
        slot_id, error = await self.manager.add_slot("2023-12-01 10:00", "Invalid Capacity", 0)
        self.assertIsNone(slot_id)
        self.assertIn("Die Kapazität muss mindestens 1 sein", error)

    async def test_book_slot_success(self):
        await self.manager.add_slot("2023-12-01 10:00", "Test Slot", 1)
        success, message = await self.manager.book_slot(1, 12345)
        self.assertTrue(success)
        self.assertEqual(message, "Buchung erfolgreich!")

        slots = await self.manager.get_user_bookings(12345)
        self.assertEqual(len(slots), 1)

    async def test_book_slot_full(self):
        await self.manager.add_slot("2023-12-01 10:00", "Full Slot", 1)
        await self.manager.book_slot(1, 111)
        success, message = await self.manager.book_slot(1, 222)
        self.assertFalse(success)
        self.assertEqual(message, "Dieser Slot ist bereits voll belegt.")

    async def test_book_slot_already_booked(self):
        await self.manager.add_slot("2023-12-01 10:00", "Repeat Slot", 2)
        await self.manager.book_slot(1, 123)
        success, message = await self.manager.book_slot(1, 123)
        self.assertFalse(success)
        self.assertEqual(message, "Du hast diesen Slot bereits gebucht.")

    async def test_cancel_booking(self):
        await self.manager.add_slot("2023-12-01 10:00", "Cancel Slot", 1)
        await self.manager.book_slot(1, 123)
        success, message = await self.manager.cancel_booking(1, 123)
        self.assertTrue(success)

        slots = await self.manager.get_user_bookings(123)
        self.assertEqual(len(slots), 0)

    async def test_delete_slot(self):
        await self.manager.add_slot("2023-12-01 10:00", "Delete Slot", 1)
        success = await self.manager.delete_slot(1)
        self.assertTrue(success)
        slots = await self.manager.get_all_slots()
        self.assertEqual(len(slots), 0)

    async def test_persistence(self):
        await self.manager.add_slot("2023-12-01 10:00", "Persist Slot", 1)
        # Create a new manager with the same file
        new_manager = BookingManager(self.test_file)
        slots = await new_manager.get_all_slots()
        self.assertEqual(len(slots), 1)
        self.assertEqual(slots[0]["description"], "Persist Slot")

    async def test_get_slot_by_id(self):
        slot_id, error = await self.manager.add_slot("2023-12-01 10:00", "Find Me", 1)
        slot = await self.manager.get_slot_by_id(slot_id)
        self.assertIsNotNone(slot)
        self.assertEqual(slot["description"], "Find Me")

        none_slot = await self.manager.get_slot_by_id(999)
        self.assertIsNone(none_slot)

if __name__ == "__main__":
    unittest.main()
