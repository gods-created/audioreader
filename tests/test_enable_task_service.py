from unittest import TestCase
from unittest.mock import MagicMock
from loguru import logger
from multiprocessing import Process
import services

class TestEnableTaskService(TestCase):
    def test_service_with_mock(self):
        services.enable_task = MagicMock()
        services.enable_task.return_value = None 
        response = services.enable_task()
        services.enable_task.assert_called_once_with()
        self.assertIsNone(response)

    def test_service(self):
        logs = []
        sink_id = logger.add(
            logs.append,
            level='DEBUG',
            format='{level} | {message}'
        )
        
        process = Process(target=services.enable_task)
        process.start()
        if process.is_alive():
            process.kill()

        logger.remove(sink_id)
        assert not 'DEBUG | Task enabled. Running...\n' in logs

        