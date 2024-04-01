import json

import pandas as pd

input_traindata = '../ft_re_csv/train.csv'
input_testdata = '../ft_re_csv/test.csv'
output_traindata = '../ft_spo_json_2/train_spo.json'
output_testdata = '../ft_spo_json_2/8_test_spo.json'


def traindataset(input_traindata, output_traindata):
    df = pd.read_csv(input_traindata)

    data = {}
    for _, row in df.iterrows():
        text = row['input']
        relation = {
            'head': row['subject'],
            'head_type': row['subject_type'],
            'relation': row['relation'],
            'tail': row['object'],
            'tail_type': row['object_type']
        }

        if text not in data:
            data[text] = {'text': text, 'relation': []}

        data[text]['relation'].append(relation)

    res = list(data.values())
    with open(output_traindata, 'w', encoding='utf-8') as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def testdataset(input_testdata, output_testdata):
    df = pd.read_csv(input_testdata)

    data = {}
    for _, row in df.iterrows():
        text = row['input']

        if text not in data:
            data[text] = {'text': text}

    res = list(data.values())
    with open(output_testdata, 'w', encoding='utf-8') as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    traindataset(input_traindata, output_traindata)
    testdataset(input_testdata, output_testdata)
