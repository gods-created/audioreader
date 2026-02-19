from os import makedirs
from os import stat
from os.path import exists, abspath
from glob import glob
from loguru import logger
from uuid import uuid4
from configs import CURRENT_PATH, TEXT_BUCKET, STORE_FILE, MODEL_NAME
from typing import Tuple, Union
from services import set_file_content, get_file_content
from vosk import Model, KaldiRecognizer
from json import loads
from wave import open as wv_open
from multiprocessing import Semaphore

def speech_to_text(audio_file_path: str) -> Tuple[bool, Union[bytes, str]]:
    status, text = False, None 

    try:
        if MODEL_NAME is None or not exists(MODEL_NAME):
            raise FileNotFoundError('Model didn\'t find')
        
        model = Model(MODEL_NAME)
        wf = wv_open(audio_file_path, 'rb')

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise Exception('Requires mono WAV 16bit')

        rec = KaldiRecognizer(model, 16000)
        text = ''

        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                result = loads(rec.Result())
                text += result.get('text', '') + '\n'

        final = loads(rec.FinalResult())
        text += final.get('text', '').strip()
        status = not status

    except FileNotFoundError as e:
        text = e

    except Exception as e:
        text = str(e)
    
    return status, text,

def audio_reader() -> None:
    makedirs(TEXT_BUCKET, exist_ok=True)

    semaphore = Semaphore(value=1)
    with semaphore:
        audio_files = sorted(
            glob(f'{CURRENT_PATH}/*.wav'),
            key=lambda x: stat(x).st_mtime
        )
        if not audio_files:
            logger.info('No audio in folder')
            return
        
        audio_files = [abspath(f) for f in audio_files]
        store_file = list({abspath(path) for path in (get_file_content(STORE_FILE) or [])})

        for audio_file in audio_files:
            if audio_file not in store_file:
                status, text = speech_to_text(audio_file)
                
                if not status:
                    logger.error(text)
                    return

                with open(f'{TEXT_BUCKET}/{uuid4()}.txt', mode='w', encoding='utf-8') as bucket:
                    bucket.write(text)

                store_file.append(audio_file)
                
        set_file_content(STORE_FILE, 'w', '\n'.join(store_file) + '\n')
    
    return

if __name__ == '__main__':
    audio_reader()

# python audio_reader.py