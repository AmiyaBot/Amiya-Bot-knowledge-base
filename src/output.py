from typing import List
from src.utils import *


def output_files(save_path: str, max_file_num: int = 100, separator: str = '\n\n'):
    index = 1
    rec = 0

    delete_dir(save_path)

    def create(name: str, contents: List[str]):
        nonlocal index, rec

        with create_file(f'{save_path}/{index}/%s.txt' % name) as file:
            file.write(separator.join(contents).strip('\n'))

        rec += 1
        if rec >= max_file_num:
            rec = 0
            index += 1

    return create
