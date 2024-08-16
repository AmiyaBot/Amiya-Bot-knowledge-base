from src.output import OutputFiles
from src.baidu.ab import AppBuilderKnowledgeBase
from src.utils import *

knowledge_base = AppBuilderKnowledgeBase('story')
book_store = OutputFiles('stories', single_file=argv('single_file', bool))


def roguelike():
    roguelike_topic_table = JsonData.get_json_data('roguelike_topic_table')
    story_review_meta_table = JsonData.get_json_data('story_review_meta_table')

    for rid, detail in roguelike_topic_table['details'].items():

        book_name = roguelike_topic_table['topics'][rid]['name']
        book_store.create(book_name, book_name, [roguelike_topic_table['topics'][rid]['lineText']])

        if book_name == '傀影与猩红孤钻':
            avgs = story_review_meta_table['actArchiveResData']['avgs']
            indexes = [
                (1, avgs['avg_rogue_1_2']),
                (2, avgs['avg_rogue_1_3']),
                (3, avgs['avg_rogue_1_4']),
                (4, avgs['avg_rogue_1_5']),
            ]

            for idx, endbook in progress(indexes, book_name):
                section_name = '%s-结局%d：%s' % (book_name, idx, endbook['desc'].strip())
                content = (
                    endbook['rawBrief']
                    + '\n\n'
                    + read_content(f'{gamedata}/story/%s.txt' % endbook['contentPath'].lower())
                )
                book_store.create(section_name, book_name, [content])
        else:
            for endbook in progress(detail['archiveComp']['endbook']['endbook'].values(), book_name):
                ending = detail['endings'][endbook['endingId']]
                section_name = '%s-结局%d：%s' % (book_name, ending['priority'] + 1, ending['name'].strip())
                content = ending['desc'] + '\n\n' + read_content(f'{gamedata}/story/%s.txt' % endbook['avgId'].lower())

                book_store.create(section_name, book_name, [content])

        for month in detail['monthSquad'].values():
            chat = detail['archiveComp']['chat']['chat'][month['chatId']]

            book_content = [month['teamDes']]

            for item in chat['clientChatItemData']:
                book_content.append(read_content(f'{gamedata}/story/%s.txt' % item['chatStoryId'].lower()))

            book_store.create('%s-%s' % (book_name, month['teamName'].strip()), book_name, book_content)


def main():
    story_review_table = JsonData.get_json_data('story_review_table')

    for item in story_review_table.values():

        if item['id'].startswith('main') or ('act' in item['id']):
            book_name = item['name']
        else:
            continue

        for sec in progress(sorted(item['infoUnlockDatas'], key=lambda n: n['storySort']), book_name):
            file = gamedata + '/story/{storyTxt}.txt'.format_map(sec)
            section_name: str = book_name + '-{storyName} {avgTag}'.format_map(sec)

            section_name = section_name.replace(':', '：')
            section_name = section_name.replace('?', '？')

            book_store.create(section_name, book_name, [read_content(file)])

    roguelike()
    book_store.done()
    knowledge_base.compare_files_and_update(book_store.result)


if __name__ == '__main__':
    main()
