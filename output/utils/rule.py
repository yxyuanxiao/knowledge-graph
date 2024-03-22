import pandas as pd
import re

pattern_map = {
    r'包括|分为|分别|等|.*是.*或是': '包含/',
    r'被定义|是': '被定义为/',
    r'定义': '定义/',
    r'开始|启动|[1-2]\d{3}': '创建时间/创建者/',
    r'本质': '等价/',
    r'采用|使用': '方法/',
    r'来自|来源': '来源/',
    r'理想|旨在|目标|目的': '目标/',
    r'是': '属于/',
    r'特点': '特点/',
    r'需要': '需要/',
    r'组成|组织': '由组成/',
    r'用于|作用': '作用/',
    r'[a-zA-Z]+': '英文名/',
    r'产生|产出': '产生'
}

data = pd.read_csv('SPO-4_副本2.csv')

for index, row in data.iterrows():
    text = row['input']
    relations = ""
    for pattern, relation in pattern_map.items():
        if re.search(pattern, text):
            relations += relation
    data.at[index, 'relation'] = relations

data.to_csv('SPO_rule.csv', index=False, encoding="utf_8_sig")