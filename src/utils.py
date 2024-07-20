import re
import os
import sys
import shutil

from src.config import Game


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


def progress(_list, name: str, display_item: bool = False):
    count = len(_list)

    def print_bar(n=None):
        p = int(curr / count * 100)
        block = int(p / 4)
        progress_line = '=' * block + ' ' * (25 - block)

        msg = f'{name}...progress: [{progress_line}] ' f'{curr}/{count} {p}%' + (f' ({n})' if display_item else '')

        print('\r', end='')
        print(msg, end='')

        sys.stdout.flush()

    curr = 0

    print_bar()
    for item in _list:
        yield item
        curr += 1
        print_bar(item)

    print()


def html_tag_format(text: str):
    if text is None:
        return ''

    for o, f in Game.html_symbol.items():
        text = text.replace(o, f)

    return remove_xml_tag(text)


def parse_template(blackboard: list, description: str):
    formatter = {'0%': lambda v: f'{round(v * 100)}%'}
    data_dict = {item['key']: item.get('valueStr') or item.get('value') for index, item in enumerate(blackboard)}

    desc = html_tag_format(description.replace('>-{', '>{'))
    format_str = re.findall(r'({(\S+?)})', desc)
    if format_str:
        for desc_item in format_str:
            key = desc_item[1].split(':')
            fd = key[0].lower().strip('-')
            if fd in data_dict:
                value = integer(data_dict[fd])

                if len(key) >= 2 and key[1] in formatter and value:
                    value = formatter[key[1]](value)

                desc = desc.replace(desc_item[0], str(value))

    return desc
