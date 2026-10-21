"""Kiểm tra param Hà Nội và cách ghép hourly thành bảng."""

import unittest

from weather.config import COLUMNS, PARAMS
from weather.transform import to_frame


class HourlyFrameTest(unittest.TestCase):
    def test_request_is_hanoi_without_api_key(self):
        self.assertEqual(PARAMS["latitude"], 21.0285)
        self.assertEqual(PARAMS["longitude"], 105.8542)
        self.assertEqual(PARAMS["timezone"], "Asia/Bangkok")
        self.assertNotIn("apikey", PARAMS)
        self.assertEqual(PARAMS["hourly"].split(","), COLUMNS[1:])

    def test_to_frame_one_row_per_hour(self):
        hourly = {
            name: ["2026-10-21T00:00", "2026-10-21T01:00"] if name == "time" else [1, 2]
            for name in COLUMNS
        }
        frame = to_frame(hourly)
        self.assertEqual(list(frame.columns), COLUMNS)
        self.assertEqual(len(frame), 2)
        self.assertEqual(frame.iloc[0]["time"], "2026-10-21T00:00")


if __name__ == "__main__":
    unittest.main()
