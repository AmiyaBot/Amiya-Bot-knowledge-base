from src.jsonData import JsonData
from src.config import gamedata
from src.output import output_files
from src.utils import *


operator_list = JsonData.get_json_data('character_table')


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


def roguelike():
    roguelike_topic_table = JsonData.get_json_data('roguelike_topic_table')
    story_review_meta_table = JsonData.get_json_data('story_review_meta_table')

    create_side = output_files('stories_roguelike')

    for rid, detail in roguelike_topic_table['details'].items():

        book_name = roguelike_topic_table['topics'][rid]['name']
        book_content = [
            f'《{book_name}》',
            roguelike_topic_table['topics'][rid]['lineText'],
        ]

        if book_name == '傀影与猩红孤钻':
            avgs = story_review_meta_table['actArchiveResData']['avgs']
            indexes = [
                (1, avgs['avg_rogue_1_2']),
                (2, avgs['avg_rogue_1_3']),
                (3, avgs['avg_rogue_1_4']),
                (4, avgs['avg_rogue_1_5']),
            ]

            for idx, endbook in progress(indexes, book_name):
                section_name = '《结局%d：%s》' % (idx, endbook['desc'])
                content = (
                    endbook['rawBrief']
                    + '\n\n'
                    + read_content(f'{gamedata}/story/%s.txt' % endbook['contentPath'].lower())
                )
                book_content.append(section_name)
                book_content.append(content)
        else:
            for endbook in progress(detail['archiveComp']['endbook']['endbook'].values(), book_name):
                ending = detail['endings'][endbook['endingId']]
                section_name = '《结局%d：%s》' % (ending['priority'] + 1, ending['name'])
                content = ending['desc'] + '\n\n' + read_content(f'{gamedata}/story/%s.txt' % endbook['avgId'].lower())

                book_content.append(section_name)
                book_content.append(content)

        for month in detail['monthSquad'].values():
            chat = detail['archiveComp']['chat']['chat'][month['chatId']]

            book_content.append('《%s》' % month['teamName'])
            book_content.append(month['teamDes'])

            for item in chat['clientChatItemData']:
                book_content.append(read_content(f'{gamedata}/story/%s.txt' % item['chatStoryId'].lower()))

        create_side(book_name, book_content)


def main():
    story_review_table = JsonData.get_json_data('story_review_table')

    create_main = output_files('stories_main')
    create_side = output_files('stories_side')

    for item in story_review_table.values():
        book_content = []
        is_main = False

        if item['id'].startswith('main'):
            chapter = item['id'].split('_')[-1]
            book_name = f'主线第 {chapter} 章：' + item['name']
            is_main = True
        else:
            if 'act' not in item['id']:
                continue
            book_name = item['name']

        for sec in progress(sorted(item['infoUnlockDatas'], key=lambda n: n['storySort']), book_name):
            file = gamedata + '/story/{storyTxt}.txt'.format_map(sec)
            section_name = '\n\n《{storyName} {avgTag}》'.format_map(sec)

            book_content.append(section_name)
            book_content.append(read_content(file))

        if is_main:
            create_main(book_name, book_content)
        else:
            create_side(book_name, book_content)


if __name__ == '__main__':
    # main()
    roguelike()
