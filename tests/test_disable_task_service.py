from unittest import TestCase
from unittest.mock import patch
from multiprocessing import Process
from loguru import logger
import services

class TestDisableTaskService(TestCase):
    def setUp(self) -> None:
        self.process = Process()
    
    @patch('services.disable_task')
    def test_service_with_mock(self, mock_object):
        mock_object.return_value = None 
        response = services.disable_task(self.process)
        mock_object.assert_called_once_with(self.process)
        self.assertIsNone(response)

    def test_service(self):
        logs = []
        sink_id = logger.add(
            logs.append,
            level='WARNING',
            format='{level} | {message}'
        )
        
        self.process.start()
        response = services.disable_task(self.process)
        logger.remove(sink_id)
        self.assertIsNone(response)
        assert 'WARNING | Process stopped.\n' in logs