import json

from typing import List, Optional
from src.baidu import BosUploader
from src.utils import *

dist_folder = './dist'


def output_files(
    out_dir: str,
    max_file_num: int = 100,
    separator: str = '\n\n',
    uploader: Optional[BosUploader] = None,
):
    index = 1
    rec = 0

    def create(name: str, contents: List[str]):
        nonlocal index, rec

        path = f'{out_dir}/{index}/{name}.txt'
        content = separator.join(contents).strip('\n')

        if uploader:
            uploader.upload_string(f'/{path}', content)
        else:
            with create_file(f'{dist_folder}/{path}') as file:
                file.write(content)

        rec += 1
        if rec >= max_file_num:
            rec = 0
            index += 1

    return create


def output_jsonl(data: list, filename: str, max_lines: int = 5000):
    index = 0
    line = 0
    file = open(f'{filename}.jsonl', 'w', encoding='utf-8')

    while data:
        item = data.pop(0)
        json_str = json.dumps(item, ensure_ascii=False)
        file.write(('\n' if line else '') + json_str)
        line += 1

        if max_lines and line >= max_lines:
            line = 0
            index += 1
            file.close()
            file = open(f'{filename}_{index}.jsonl', 'w', encoding='utf-8')

    file.close()
