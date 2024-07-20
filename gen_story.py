from src.jsonData import JsonData
from src.config import gamedata
from src.output import output_files
from src.utils import *


def read_content(path: str):
    with open(path, mode='r', encoding='utf-8') as f:
        content = f.read()

    paragraph = 0
    text = []

    for row in content.split('\n'):
        line = row.replace('Dr.{@nickname}', '博士')

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
        else:
            if paragraph != 0:
                text.append('')
                paragraph = 0

            text.append(line)

    return '\n'.join(text).strip('\n')


def main():
    story_review_table = JsonData.get_json_data('story_review_table')

    create = output_files('dist/game_stories')

    for item in story_review_table.values():
        if item['id'].startswith('main'):
            chapter = item['id'].split('_')[-1]
            book_name = f'主线第 {chapter} 章：' + item['name']
            book_content = []

            for sec in progress(sorted(item['infoUnlockDatas'], key=lambda n: n['storySort']), book_name):
                file = gamedata + '/gamedata/story/{storyTxt}.txt'.format_map(sec)
                section_name = '\n\n《{storyName} {avgTag}》'.format_map(sec)

                book_content.append(section_name)
                book_content.append(read_content(file))

            create(book_name, book_content)


if __name__ == '__main__':
    main()
