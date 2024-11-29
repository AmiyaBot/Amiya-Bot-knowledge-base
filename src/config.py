import json

with open('config/gamedata.json', mode='r', encoding='utf-8') as f:
    gamedata = json.load(f)['gamedata']


class Game:
    classes = {
        'CASTER': '术师',
        'MEDIC': '医疗',
        'PIONEER': '先锋',
        'SNIPER': '狙击',
        'SPECIAL': '特种',
        'SUPPORT': '辅助',
        'TANK': '重装',
        'WARRIOR': '近卫',
    }
    token_classes = {
        'TOKEN': '召唤物',
        'TRAP': '装置',
    }
    high_star = {
        '5': '资深干员',
        '6': '高级资深干员',
    }
    types = {
        'ALL': '不限部署位',
        'MELEE': '近战位',
        'RANGED': '远程位',
    }
    html_symbol = {
        '<替身>': '替身',
        '<支援装置>': '支援装置',
    }
    sp_type = {
        'INCREASE_WITH_TIME': '自动回复',
        'INCREASE_WHEN_ATTACK': '攻击回复',
        'INCREASE_WHEN_TAKEN_DAMAGE': '受击回复',
        1: '自动回复',
        2: '攻击回复',
        4: '受击回复',
        8: '被动',
    }
    skill_type = {
        'PASSIVE': '被动',
        'MANUAL': '手动触发',
        'AUTO': '自动触发',
        0: '被动',
        1: '手动触发',
        2: '自动触发',
    }
    skill_level = {
        1: '等级1',
        2: '等级2',
        3: '等级3',
        4: '等级4',
        5: '等级5',
        6: '等级6',
        7: '等级7',
        8: '等级8（专精1）',
        9: '等级9（专精2）',
        10: '等级10（专精3）',
    }
    attrs = {
        'maxHp': '最大生命值',
        'atk': '攻击力',
        'def': '防御力',
        'magicResistance': '魔法抗性',
        'attackSpeed': '攻击速度',
        'baseAttackTime': '攻击间隔',
        'blockCnt': '阻挡数',
        'cost': '部署费用',
        'respawnTime': '再部署时间',
    }
    attrs_unit = {
        'baseAttackTime': '秒',
        'respawnTime': '秒',
    }
