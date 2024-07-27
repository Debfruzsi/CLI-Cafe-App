import unittest
import os
import csv
from io import StringIO
from unittest.mock import patch, mock_open

# Import the function to be tested
from final_week6.mini_project_week6 import save_to_csv

class TestSaveToCsv(unittest.TestCase):

    def setUp(self):
        # This method can set up test data that is common to multiple tests
        self.file_path = 'test.csv'
        self.data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': 25},
        ]
        self.expected_csv_content = (
            'name,age\r\n'
            'Alice,30\r\n'
            'Bob,25\r\n'
        )

    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_csv(self, mock_file):
        # Act: Call the function with a mock file path
        save_to_csv(self.file_path, self.data)
        
        # Assert: Check that open was called correctly and the right content was written
        mock_file.assert_called_once_with(self.file_path, 'w', newline='')
        handle = mock_file()
        handle.write.assert_any_call('name,age\r\n')
        handle.write.assert_any_call('Alice,30\r\n')
        handle.write.assert_any_call('Bob,25\r\n')

        # Additionally, we can check the overall content if necessary
        handle.write.assert_has_calls([
            unittest.mock.call('name,age\r\n'),
            unittest.mock.call('Alice,30\r\n'),
            unittest.mock.call('Bob,26\r\n'),
        ], any_order=False)

    @patch('builtins.open', new_callable=mock_open)
    def test_save_empty_data_to_csv(self, mock_file):
        # Arrange: Test case with empty data
        empty_data = []
        expected_csv_content = ''  # No content for empty data

        # Act: Call the function with empty data
        save_to_csv(self.file_path, empty_data)
        
        # Assert: Check that open was not called at all since data is empty
        mock_file.assert_not_called()  # Ensure that the open function was never called


    def tearDown(self):
        # Clean up actions if needed
        pass

if __name__ == '__main__':
    unittest.main()
