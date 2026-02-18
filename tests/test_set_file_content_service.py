from unittest import TestCase
from unittest.mock import patch
from os.path import exists
from os import remove
import services

class TestSetFileContentService(TestCase):
    def setUp(self) -> None:
        self.filename = '.state'
        self.args = (
            self.filename,
            'w',
            '1'
        )
    
    @patch('services.set_file_content')
    def test_service_with_mock(self, mock_object):
        mock_object.return_value = None 
        response = services.set_file_content(*self.args)
        mock_object.assert_called_once_with(*self.args)
        self.assertIsNone(response)

    def test_service(self):
        response = services.set_file_content(*self.args)
        self.assertIsNone(response)
        self.assertTrue(exists(self.filename))

    def tearDown(self) -> None:
        if exists(self.filename):
            remove(self.filename)