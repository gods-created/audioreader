from .set_file_content import set_file_content as set_file_content_service
from .get_file_content import get_file_content as get_file_content_service
from loguru import logger
from configs import STATE_FILE
from re import match
from multiprocessing import Process
from typing import Optional

def disable_task(process: Optional[Process]) -> None:
    '''Останавливает выполнение периодической задачи.'''
    content = get_file_content_service(STATE_FILE) or ['0']
    if not match('0', content[0]):
        set_file_content_service(STATE_FILE, 'w', '0')
    
    if process and process.is_alive():
        process.kill()
        logger.warning('Process stopped.')
        
    logger.debug('Task disabled.')