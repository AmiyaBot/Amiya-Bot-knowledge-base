from .tools import *
from .jsonData import JsonData


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


def check_nickname(text: str):
    for n in [
        'Dr.{@nickname}',
        '{@nickname}博士',
        '{@nickname}',
        'Dr.{@Nickname}',
        '{@Nickname}博士',
        '{@Nickname}',
    ]:
        text = text.replace(n, '博士')
    return text


def read_content(path: str):
    operator_list = JsonData.get_json_data('character_table')

    with open(path, mode='r', encoding='utf-8') as f:
        content = f.read()

    paragraph = 0
    text = []

    for row in content.split('\n'):
        line = check_nickname(row)

        if line.startswith('['):
            r = re.search(r'^\[name="(\S+)?"](.*)', line)
            if r:
                if paragraph != 1:
                    text.append('')
                    paragraph = 1

                text.append(f'{r.group(1) or "（未知）"}：“{r.group(2).strip()}”')
                continue

            r = re.search(r'text="([^"]+)"', line)
            if r:
                if paragraph != 2:
                    text.append('')
                    paragraph = 2

                text.append(r.group(1).replace('\\n', ''))
                continue

            r = re.search(r'^\[Dialog\(head="(\S+)",.*](.*)', line)
            if r:
                if paragraph != 3:
                    text.append('')
                    paragraph = 3

                char = operator_list[r.group(1)] if r.group(1) in operator_list else None
                text.append(f'{char["name"] if char else "（未知）"}：“{r.group(2).strip()}”')
                continue

        else:
            if paragraph != 0:
                text.append('')
                paragraph = 0

            text.append(line)

    return remove_xml_tag('\n'.join(text).strip('\n'))
