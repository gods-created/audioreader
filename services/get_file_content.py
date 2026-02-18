from typing import List, Optional, Union
from os.path import exists

def get_file_content(filename: str) -> Optional[List[Union[str, bytes]]]:
    if not exists(filename):
        return None
    
    with open(filename) as f:
        return f.readlines()
    