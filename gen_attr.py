from src.output import OutputFiles
from src.baidu.appBuilder import AppBuilderKnowledgeBase
from src.utils import *

knowledge_base = AppBuilderKnowledgeBase('attr')
book_store = OutputFiles(
    'attrs',
    single_file=argv('single_file', bool),
    separator='\n\n===separator===\n\n',
)


def main():
    operator_list = JsonData.get_json_data('character_table')
    team_table = JsonData.get_json_data('handbook_team_table')
    sub_classes = JsonData.get_json_data('uniequip_table')['subProfDict']

    for char_id, char in progress(operator_list.items(), '干员属性'):
        if char['profession'] in Game.token_classes:
            continue

        char_name = char['name']
        char_desc = html_tag_format(char['description'])

        classes = Game.classes[char['profession']]
        classes_sub = sub_classes[char['subProfessionId']]['subProfessionName']

        if classes_sub == '驭械术师':
            char_desc = '初始携带1个浮游单元，浮游单元初始造成相当于干员攻击力20%的法术伤害，每次对上次攻击的同一目标进行攻击时该数值增加15，上限110%（即通常情况下需叠加6次才能达到上限）。'

        group_id = char['groupId']
        group = team_table[group_id]['powerName'] if group_id in team_table else '无'

        max_phases = char['phases'][-1]
        max_attr = max_phases['attributesKeyFrames'][-1]['data']

        content = f'{char_name}\n职业：{classes_sub}（{classes}），{char_desc}\n阵营：{group}\n' + '\n'.join(
            [f'{n}：{max_attr[k]}%s' % Game.attrs_unit.get(k, '') for k, n in Game.attrs.items()]
        )

        talents = []
        if char['talents']:
            for index, item in enumerate(char['talents']):
                max_item = item['candidates'][-1]
                if max_item['name']:
                    text = '第%d天赋：%s，效果为%s。' % (
                        index + 1,
                        max_item['name'],
                        html_tag_format(max_item['description']),
                    )
                    text = re.sub(r'（[+-]\d+(\.\d+)?%?）', '', text)
                    text = re.sub(r'\([+-]\d+(\.\d+)?%?\)', '', text)

                    talents.append(text)

        content += ('\n\n' + '\n'.join(talents)) if talents else ''

        book_store.create(char_name, '干员属性', [content])

    book_store.done()
    knowledge_base.compare_files_and_update(book_store.result, separator=book_store.separator)


if __name__ == '__main__':
    main()
