import pandas as pd
import json

def traindataset():
    df = pd.read_csv('../ft_re_csv/train.csv')

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
    with open('../ft_re_json/train.json', 'w', encoding='utf-8') as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False)+'\n')


def testdataset():
    df = pd.read_csv('../ft_re_csv/test.csv')

    data = {}
    for _, row in df.iterrows():
        text = row['input']

        if text not in data:
            data[text] = {'text': text}

    res = list(data.values())
    with open('../ft_re_json/test.json', 'w', encoding='utf-8') as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False)+'\n')

if __name__ == '__main__':
    traindataset()
    #testdataset()