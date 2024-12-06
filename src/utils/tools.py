import re
import os
import sys
import shutil

from src.config import Game


def argv(name, formatter=str):
    key = f'--{name}'
    if key in sys.argv:
        index = sys.argv.index(key) + 1

        if index >= len(sys.argv):
            return True

        if sys.argv[index].startswith('--'):
            return True
        else:
            return formatter(sys.argv[index])


def integer(value):
    if type(value) is float and int(value) == value:
        value = int(value)
    return value


def remove_xml_tag(text: str):
    return re.compile(r'<[^>]+>', re.S).sub('', text)


def replace_text(text: str):
    text = remove_xml_tag(text)
    text = text.replace('\\n', '，')
    return text


def split_and_concatenate(input_list: list, max_length: int = 1200):
    if not input_list:
        return []

    concatenated = ''
    result = []

    for item in input_list:
        if len(concatenated) + len(item) >= max_length:
            result.append(concatenated)
            concatenated = item
        else:
            concatenated += item

    if concatenated:
        result.append(concatenated)

    return result


def create_dir(path: str, is_file: bool = False):
    if is_file:
        path = os.path.dirname(path)

    if path and not os.path.exists(path):
        os.makedirs(path)

    return path


def delete_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def create_file(path):
    create_dir(path, is_file=True)
    return open(path, mode='w', encoding='utf-8')


def progress(_list, name: str):
    count = len(_list)

    def print_bar():
        p = int(curr / count * 100)
        block = int(p / 4)
        progress_line = '=' * block + ' ' * (25 - block)

        msg = f'{name} [{progress_line}] ' f'{curr}/{count} {p}%'

        print('\r', end='')
        print(msg, end='')

        sys.stdout.flush()

    curr = 0

    print_bar()
    for item in _list:
        yield item
        curr += 1
        print_bar()

    print()


def html_tag_format(text: str):
    if text is None:
        return ''

    for o, f in Game.html_symbol.items():
        text = text.replace(o, f)

    return remove_xml_tag(text).replace('\n', '。').replace('\\n', '。')


def pascal_case_to_snake_case(camel_case: str):
    snake_case = re.sub(r'(?P<key>[A-Z])', r'_\g<key>', camel_case)
    return snake_case.lower().strip('_')


def snake_case_to_pascal_case(snake_case: str):
    words = snake_case.split('_')
    return ''.join(word.title() if i > 0 else word.lower() for i, word in enumerate(words))
