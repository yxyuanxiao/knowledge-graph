import json
import pandas as pd
from json import JSONDecodeError

with open("config.json") as f:
    cfg = json.load(f)


def spo_task(input_path, output_path):
    def_relation = cfg['relation']
    datas = []
    with open(input_path, 'r', encoding='utf-8') as reader:
        for i, line in enumerate(reader):
            data = json.loads(line)
            instruction = json.loads(data["instruction"])
            input = instruction["input"]
            try:
                relations = json.loads(data["output"])
            except JSONDecodeError as e:
                print(e)
                print(input)
                print(data["output"])
            for relation in relations:
                if relations[relation] is None:
                    continue
                if relation not in def_relation:
                    print(i)
                    print(input)
                    print(relations[relation])
                    continue
                for spo in relations[relation]:
                    try:
                        subject = spo["subject"]
                        object = spo["object"]
                        datas.append([input, subject, relation, object])
                    except TypeError as e:
                        print(e)
                        print(input)
                        print(spo)
                    except KeyError as e:
                        print(e)
                        print(input)
                        print(spo)
    datas = pd.DataFrame(datas, columns=["input", "subject", "relation", "object"])
    datas.to_csv(output_path, index=False, encoding="utf_8_sig")


def re_task(input_path, output_path):
    def_relation = cfg['relation']
    datas = []
    with open(input_path, 'r', encoding='utf-8') as reader:
        for i, line in enumerate(reader):
            data = json.loads(line)
            instruction = json.loads(data["instruction"])
            input = instruction["input"]
            try:
                relations = json.loads(data["output"])
            except JSONDecodeError as e:
                print(e)
                print(input)
                print(data["output"])
            for relation in relations:
                if relations[relation] is None:
                    continue
                if relation not in def_relation:
                    print(i)
                    print(input)
                    print(relations[relation])
                    continue
                for spo in relations[relation]:
                    try:
                        subject = spo["head"]
                        object = spo["tail"]
                        datas.append([input, subject, relation, object])
                    except TypeError as e:
                        print(e)
                        print(input)
                        print(spo)
                    except KeyError as e:
                        print(e)
                        print(input)
                        print(spo)
    datas = pd.DataFrame(datas, columns=["input", "subject", "relation", "object"])
    datas.to_csv(output_path, index=False, encoding="utf_8_sig")


if __name__ == '__main__':
    assert len(cfg["input_path"]) == len(cfg["output_path"])
    for input_path, output_path in zip(cfg["input_path"], cfg["output_path"]):
        spo_task(input_path, output_path)
