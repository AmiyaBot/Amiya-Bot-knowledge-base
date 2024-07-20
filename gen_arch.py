from src.jsonData import JsonData
from src.output import output_files
from src.utils import *


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

    create = output_files('dist/operators_stories', separator='\n\n===分隔符===\n\n')

    for char_id, char in progress(operator_list.items(), 'operators'):
        if char['profession'] in Game.token_classes:
            continue

        trait = replace_text(char['description'])
        if char['trait']:
            max_trait = char['trait']['candidates'][-1]
            trait = parse_template(max_trait['blackboard'], max_trait['overrideDescripton'] or trait)

        operators_stories = [
            '\n'.join(
                [
                    '【干员代号】' + char['name'],
                    '【星级】' + char['rarity'].split('_')[-1],
                    '【主职业】' + Game.classes[char['profession']],
                    '【分支职业】' + sub_classes[char['subProfessionId']]['subProfessionName'],
                    '【分支职业特性】' + trait,
                    '【简介】' + (char['itemUsage'] or '无'),
                    '【印象】' + (char['itemDesc'] or '无'),
                ]
            )
        ]

        if char_id in stories_data:
            for item in stories_data[char_id]['storyTextAudio']:
                operators_stories.append(item['stories'][0]['storyText'])

        if char_id in equips_rel:
            for m_id in equips_rel[char_id]:
                module = modules_list[m_id]
                operators_stories.append('《{uniEquipName}》\n{uniEquipDesc}'.format(**module))

        if char_id in voice_map:
            operators_stories.append(
                '《干员%s-语录》\n%s'
                % (
                    char['name'],
                    '\n'.join(
                        [
                            '“%s”' % item['voiceText']
                            for item in voice_map.get(char_id)
                            if '明日方舟' not in item['voiceText']
                        ]
                    ),
                )
            )

        create(char['name'], operators_stories)


if __name__ == '__main__':
    main()
