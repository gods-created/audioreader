def set_file_content(filename: str, mode: str, content: str) -> None:
    with open(filename, mode=mode) as f:
        f.write(content + '\n')