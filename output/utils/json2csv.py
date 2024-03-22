import json
import pandas as pd
from tqdm import tqdm
from json import JSONDecodeError

def_relation = ["属于", "包含", "等价", "中文名", "英文名", "源于", "被定义为", "研究", "依靠", "实现"]

path = "Baichuan2-7B-SPO-4_output.json"
datas = []
with open(path, 'r', encoding='utf-8') as reader:
    for i, line in enumerate(reader):
        data = json.loads(line)
        try:
            relations = json.loads(data["output"])
        except JSONDecodeError as e:
            print(e)
            print(i)
            print(data["output"])
        instruction = json.loads(data["instruction"])
        for relation in relations:
            if relations[relation] is None or relation not in def_relation:
                continue
            for spo in relations[relation]:
                try:
                    subject = spo["subject"]
                    object = spo["object"]
                    input = instruction["input"]
                    datas.append([input, subject, relation, object])
                except TypeError as e:
                    print(e)
                    print(spo)
                except KeyError as e:
                    print(e)
                    print(spo)
datas = pd.DataFrame(datas, columns=["input", "subject", "relation", "object"])
datas.to_csv("SPO-4.csv", index=False, encoding="utf_8_sig")