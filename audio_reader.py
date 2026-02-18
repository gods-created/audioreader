from os import makedirs
from os import stat
from glob import glob
from loguru import logger
from uuid import uuid4
from configs import CURRENT_PATH, TEXT_BUCKET, STORE_FILE, OPENAI_API_KEY
from typing import Tuple
from openai import OpenAI, APIStatusError, APIConnectionError, APITimeoutError, BadRequestError
from services import set_file_content, get_file_content
from re import match

def speech_to_text(audio_file_path: str) -> Tuple[bool, str]:
    status, text = False, None 

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        with open(audio_file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file,
                response_format='verbose_json',
                language='uk'
            )
            
        text = '\n'.join([item.text for item in response.segments])
        status = not status

    except (APIStatusError, APIConnectionError, APITimeoutError, BadRequestError, ) as e:
        text = e.message

    except Exception as e:
        text = str(e)

    return status, text,

def audio_reader() -> None:
    makedirs(TEXT_BUCKET, exist_ok=True)

    audio_files = sorted(
        glob(f'{CURRENT_PATH}/*.wav') + glob(f'{CURRENT_PATH}/*.mp3'),
        key=lambda x: stat(x).st_mtime
    )

    if not audio_files:
        logger.info('No audio in folder')
        return
    
    store_file = get_file_content(STORE_FILE) or []
    for audio_file in audio_files:
        if any([match(audio_file, str(item)) for item in store_file]):
            continue

        status, text = speech_to_text(audio_file)
        
        if not status:
            logger.error(text)
            return

        with open(f'{TEXT_BUCKET}/{uuid4()}.txt', mode='w') as file:
            file.write(text)

        set_file_content(STORE_FILE, 'a', audio_file)

    return

if __name__ == '__main__':
    audio_reader()

# python audio_reader.py