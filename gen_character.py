from src.output import OutputFiles
from src.baidu.appBuilder import AppBuilderKnowledgeBase
from src.utils import *

knowledge_base = AppBuilderKnowledgeBase('character')
book_store = OutputFiles(
    'characters',
    single_file=argv('single_file', bool),
    separator='\n\n===separator===\n\n',
)


def main():
    operator_list = JsonData.get_json_data('character_table')
    sub_classes = JsonData.get_json_data('uniequip_table')['subProfDict']
    stories_data = JsonData.get_json_data('handbook_info_table')['handbookDict']
    voice_data = JsonData.get_json_data('charword_table')
    equips = JsonData.get_json_data('uniequip_table')

    equips_rel = equips['charEquip']
    modules_list = equips['equipDict']
    voice_map = {}

    for n, item in voice_data['charWords'].items():
        char_id = item['wordKey']

        if char_id not in voice_map:
            voice_map[char_id] = []

        voice_map[char_id].append(item)

    for char_id, char in progress(operator_list.items(), '干员资料'):
        if char['profession'] in Game.token_classes:
            continue

        trait = replace_text(char['description'])
        if char['trait']:
            max_trait = char['trait']['candidates'][-1]
            trait = parse_template(max_trait['blackboard'], max_trait['overrideDescripton'] or trait)

        char_name = char['name']

        book_store.create(
            char_name,
            char_name,
            [
                '\n'.join(
                    [
                        '【干员代号】' + char_name,
                        '【星级】' + char['rarity'].split('_')[-1],
                        '【主职业】' + Game.classes[char['profession']],
                        '【分支职业】' + sub_classes[char['subProfessionId']]['subProfessionName'],
                        '【分支职业特性】' + trait,
                        '【简介】' + (char['itemUsage'] or '无'),
                        '【印象】' + (char['itemDesc'] or '无'),
                    ]
                )
            ],
        )

        if char_id in stories_data:
            for item in stories_data[char_id]['storyTextAudio']:
                book_store.create(
                    char_name + '-' + item['storyTitle'],
                    char_name,
                    [item['stories'][0]['storyText']],
                )

            for item in stories_data[char_id]['handbookAvgList']:
                name = char_name + '-' + item['storySetName']
                book_content = []

                for n in item['avgList']:
                    book_content.append(n['storyIntro'])
                    book_content.append(read_content(f'{gamedata}/story/[uc]' + n['storyInfo'] + '.txt'))
                    book_content.append(read_content(f'{gamedata}/story/' + n['storyTxt'] + '.txt'))

                book_store.create(name, char_name, book_content)

        if char_id in equips_rel:
            for m_id in equips_rel[char_id]:
                module = modules_list[m_id]
                book_store.create(
                    char_name + '-' + module['uniEquipName'],
                    char_name,
                    [module['uniEquipDesc']],
                )

        if char_id in voice_map:
            book_store.create(
                char_name + '-语音记录',
                char_name,
                [
                    '\n'.join(
                        [
                            char_name + '：“%s”' % item['voiceText']
                            for item in voice_map.get(char_id)
                            if '明日方舟' not in item['voiceText']
                        ]
                    )
                ],
            )

    book_store.done()
    knowledge_base.compare_files_and_update(book_store.result, separator=book_store.separator)


if __name__ == '__main__':
    main()
