import unittest

from app.routes.businesses import normalize_booking_status


class BookingStatusNormalizationTests(unittest.TestCase):
    def test_normalizes_spanish_statuses_to_canonical_values(self) -> None:
        self.assertEqual(normalize_booking_status("aceptado"), "accepted")
        self.assertEqual(normalize_booking_status("rechazado"), "rejected")
        self.assertEqual(normalize_booking_status("cancelado"), "canceled")
        self.assertEqual(normalize_booking_status("pending"), "pending")


if __name__ == "__main__":
    unittest.main()
