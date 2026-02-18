from unittest import TestCase
from unittest.mock import MagicMock 
from loguru import logger
import audio_reader

class TestAudioReader(TestCase):
    def test_reader_with_mock(self):
        audio_reader.audio_reader = MagicMock()
        audio_reader.audio_reader.return_value = None
        response = audio_reader.audio_reader()
        audio_reader.audio_reader.assert_called_once_with()
        self.assertIsNone(response)

    def test_reader(self):
        logs = []
        sick_id = logger.add(
            sink=logs.append,
            level='INFO',
            format='{level} | {message}'
        )

        callable = audio_reader.audio_reader
        callable()

        logger.remove()

        assert 'INFO | No audio in folder\n' in logs