import unittest
from unittest.mock import patch, MagicMock
import app  # Make sure this imports your main application file

class TestActivityTracker(unittest.TestCase):

    @patch('app.take_screenshot')
    @patch('app.upload_to_s3')
    def test_screenshot_capture(self, mock_upload, mock_screenshot):
        mock_screenshot.return_value = 'screenshot_test.png'
        file_name = app.take_screenshot()
        self.assertEqual(file_name, 'screenshot_test.png')
        mock_screenshot.assert_called_once()

    @patch('app.check_internet_connection')
    @patch('app.upload_to_s3')
    def test_upload_with_no_internet(self, mock_upload, mock_check):
        mock_check.return_value = False  # Simulate no internet connection
        app.upload_to_s3('test_file.png', 'your-s3-bucket')
        self.assertIn('test_file.png', app.upload_queue)  # File should be queued

    @patch('app.check_internet_connection')
    @patch('app.upload_to_s3')
    def test_upload_with_internet(self, mock_upload, mock_check):
        mock_check.return_value = True  # Simulate internet connection
        mock_upload.return_value = None  # Simulate successful upload
        app.upload_to_s3('test_file.png', 'your-s3-bucket')
        mock_upload.assert_called_once_with('test_file.png', 'your-s3-bucket')

    def test_instance_management(self):
        # Create a PID file
        app.check_single_instance()  # Should create a PID file
        self.assertTrue(os.path.isfile(app.pid_file))

        # Attempt to create another instance (should exit)
        with self.assertRaises(SystemExit):
            app.check_single_instance()

        # Cleanup PID file
        app.cleanup()
        self.assertFalse(os.path.isfile(app.pid_file))

    @patch('app.psutil.sensors_battery')
    def test_battery_status(self, mock_battery):
        # Mock battery status
        mock_battery.return_value = MagicMock(percent=15, power_plugged=False)
        percent, is_plugged = app.check_battery_status()
        self.assertEqual(percent, 15)
        self.assertFalse(is_plugged)

    def test_log_activity(self):
        activity = "Mouse moved"
        app.log_activity(activity)
        with open(app.activity_log_file, 'r') as f:
            lines = f.readlines()
        self.assertIn(activity, lines[-1])  # Check last log entry

if __name__ == '__main__':
    unittest.main()
