from src.output import OutputFiles
from src.baidu.appBuilder import AppBuilderKnowledgeBase
from src.utils import *

knowledge_base = AppBuilderKnowledgeBase('skill')
book_store = OutputFiles(
    'skills',
    single_file=argv('single_file', bool),
    separator='\n\n===separator===\n\n',
)


def main():
    operator_list = JsonData.get_json_data('character_table')
    skill_data = JsonData.get_json_data('skill_table')

    for char_id, char in progress(operator_list.items(), '干员技能'):
        if char['profession'] in Game.token_classes:
            continue

        char_name = char['name']
        contents = []

        if char['talents']:
            for index, item in enumerate(char['talents']):
                max_item = item['candidates'][-1]
                if max_item['name']:
                    contents.append(
                        '%s第%d天赋：%s，效果为%s。'
                        % (
                            char_name,
                            index + 1,
                            max_item['name'],
                            html_tag_format(max_item['description']),
                        )
                    )

        for index, item in enumerate(char['skills']):
            code = item['skillId']

            if code not in skill_data:
                continue

            detail = skill_data[code]

            if bool(detail) is False:
                continue

            skill_desc = f'{char_name}{index + 1}技能：%s，%s，%s，' % (
                detail['levels'][0]['name'],
                Game.skill_type[detail['levels'][0]['skillType']],
                Game.sp_type[detail['levels'][0]['spData']['spType']],
            )

            # for lev, desc in enumerate(detail['levels']):
            #     description = parse_template(desc['blackboard'], desc['description'])
            #     skill_desc += '%s，初始SP：%d，SP消耗：%d，技能持续时间：%d秒，最大充能次数：%d，技能效果：%s；' % (
            #         Game.skill_level[lev + 1],
            #         desc['spData']['initSp'],
            #         desc['spData']['spCost'],
            #         integer(desc['duration']),
            #         desc['spData']['maxChargeTime'],
            #         description.replace('\\n', '\n').replace('\n', '。'),
            #     )

            desc = detail['levels'][-1]
            description = parse_template(desc['blackboard'], desc['description'])
            skill_desc += '初始SP：%d，SP消耗：%d，技能持续时间：%d秒，最大充能次数：%d，技能效果：%s；' % (
                desc['spData']['initSp'],
                desc['spData']['spCost'],
                integer(desc['duration']),
                desc['spData']['maxChargeTime'],
                description.replace('\\n', '\n').replace('\n', '。'),
            )

            contents.append(skill_desc)

        book_store.create(char['name'], char['name'], contents)

    book_store.done()
    knowledge_base.compare_files_and_update(book_store.result, separator=book_store.separator)


if __name__ == '__main__':
    main()
