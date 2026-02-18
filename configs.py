from os import getcwd, getenv

STATE_FILE = '.state'
STORE_FILE = '.store'
CURRENT_PATH = getcwd()
TEXT_BUCKET = 'documents'
OPENAI_API_KEY = getenv('OPENAI_API_KEY')