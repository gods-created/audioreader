from unittest import TestCase
from unittest.mock import patch
import services

class TestGetFileContentService(TestCase):
    def setUp(self) -> None:
        self.filename = '.state'

    @patch('services.get_file_content')
    def test_service_with_mock(self, mock_object):
        mock_object.return_value = None
        response = services.get_file_content(self.filename)
        mock_object.assert_called_once_with(self.filename)
        self.assertIsNone(response)

    def test_service(self):
        response = services.get_file_content(self.filename)
        inst = isinstance(response, list) if response is not None else None
        self.assertIn(inst, [None, True])