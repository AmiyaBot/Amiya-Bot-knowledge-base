from src.jsonData import JsonData
from src.output import output_files
from src.utils import *


def main():
    operator_list = JsonData.get_json_data('character_table')
    skill_data = JsonData.get_json_data('skill_table')

    create = output_files('operators_skills', separator='\n\n===分隔符===\n\n')

    with open('prompts/skill.txt', mode='r', encoding='utf-8') as f:
        skill_prompts = f.read()

    for char_id, char in progress(operator_list.items(), 'operators'):
        if char['profession'] in Game.token_classes:
            continue

        operators_skills = [
            '【干员代号】' + char['name'],
        ]

        talents = []
        if char['talents']:
            for index, item in enumerate(char['talents']):
                max_item = item['candidates'][-1]
                if max_item['name']:
                    talents.append(
                        '【第%d天赋】%s：%s'
                        % (
                            index + 1,
                            max_item['name'],
                            html_tag_format(max_item['description']),
                        )
                    )
        if talents:
            operators_skills.append('\n'.join(talents))

        for index, item in enumerate(char['skills']):
            code = item['skillId']

            if code not in skill_data:
                continue

            detail = skill_data[code]

            if bool(detail) is False:
                continue

            skill_desc = [
                f'【{index + 1}技能】【%s】【%s】%s'
                % (
                    Game.skill_type[detail['levels'][0]['skillType']],
                    Game.sp_type[detail['levels'][0]['spData']['spType']],
                    detail['levels'][0]['name'],
                ),
            ]

            for lev, desc in enumerate(detail['levels']):
                description = parse_template(desc['blackboard'], desc['description'])
                desc_text = '%s，初始SP：%d，SP消耗：%d，技能持续时间：%d秒，最大充能次数：%d，技能效果：%s；' % (
                    Game.skill_level[lev + 1],
                    desc['spData']['initSp'],
                    desc['spData']['spCost'],
                    integer(desc['duration']),
                    desc['spData']['maxChargeTime'],
                    description.replace('\\n', '\n').replace('\n', '。'),
                )
                skill_desc.append(desc_text)

            operators_skills.append('\n'.join(skill_desc))

        operators_skills.append(skill_prompts)

        create(char['name'], operators_skills)


if __name__ == '__main__':
    main()
