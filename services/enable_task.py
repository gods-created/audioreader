from time import sleep
from .set_file_content import set_file_content as set_file_content_service
from .get_file_content import get_file_content as get_file_content_service
from configs import STATE_FILE
from loguru import logger
from threading import Thread
from re import match

def enable_task() -> None:
    '''Запускает периодическое выполнение скрипта каждую минуту.'''

    if (content := get_file_content_service(STATE_FILE)) is None or match('0', content[0]):
        set_file_content_service(STATE_FILE, 'w', '1')
        content = get_file_content_service(STATE_FILE)

    try:
        if match('1', content[0]):
            logger.debug('Task enabled. Running...')

            import audio_reader
            thread = Thread(target=audio_reader.audio_reader)
            thread.start()
            
            sleep(10)
            return enable_task()

    except KeyboardInterrupt:
        logger.warning('Task stopped by user.')

    return 