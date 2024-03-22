import pandas as pd
import json

df = pd.read_csv('spo.csv')

data = {}
for _, row in df.iterrows():
    text = row['input']
    relation = {
        'head': row['subject'],
        'relation': row['relation'],
        'tail': row['object']
    }

    if text not in data:
        data[text] = {'text': text, 'relation': []}

    data[text]['relation'].append(relation)

res = list(data.values())
with open('data.json', 'w', encoding='utf-8') as f:
    for r in res:
        f.write(json.dumps(r, ensure_ascii=False)+'\n')
