import unittest
import os
from booking_manager import BookingManager

class TestBookingManager(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.test_db = 'test_bookings.json'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.manager = BookingManager(self.test_db)

    async def asyncTearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    async def test_add_slot(self):
        slot_id = await self.manager.add_slot('2023-12-24', '18:00')
        self.assertEqual(slot_id, 1)
        slots = await self.manager.get_all_slots()
        self.assertEqual(len(slots), 1)
        self.assertEqual(slots[0]['date'], '2023-12-24')

    async def test_book_slot(self):
        await self.manager.add_slot('2023-12-24', '18:00')
        success, message = await self.manager.book_slot(1, 123, 'TestUser')
        self.assertTrue(success)

        slots = await self.manager.get_available_slots()
        self.assertEqual(len(slots), 0)

        bookings = await self.manager.get_user_bookings(123)
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0]['slot_id'], 1)

    async def test_cancel_booking(self):
        await self.manager.add_slot('2023-12-24', '18:00')
        await self.manager.book_slot(1, 123, 'TestUser')

        success, message = await self.manager.cancel_booking(1, 123)
        self.assertTrue(success)

        slots = await self.manager.get_available_slots()
        self.assertEqual(len(slots), 1)
        self.assertTrue(slots[0]['available'])

    async def test_delete_slot(self):
        await self.manager.add_slot('2023-12-24', '18:00')
        await self.manager.delete_slot(1)
        slots = await self.manager.get_all_slots()
        self.assertEqual(len(slots), 0)

if __name__ == '__main__':
    unittest.main()
