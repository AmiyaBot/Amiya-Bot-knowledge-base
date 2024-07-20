import os
import json

from src.config import gamedata


class JsonData:
    cache = {}

    @classmethod
    def get_json_data(cls, name: str, folder: str = 'excel'):
        if name not in cls.cache:
            path = f'{gamedata}/{folder}/{name}.json'
            if os.path.exists(path):
                with open(path, mode='r', encoding='utf-8') as src:
                    cls.cache[name] = json.load(src)
            else:
                return {}

        return cls.cache[name]

    @classmethod
    def create_jsonl(cls, data: list, filename: str, max_lines: int = 5000):
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
