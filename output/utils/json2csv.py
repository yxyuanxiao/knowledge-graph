import json
import pandas as pd
from tqdm import tqdm
from json import JSONDecodeError


def spo_task(path):
    def_relation = ["属于", "包含", "等价", "中文名", "英文名", "源于", "被定义为", "研究", "依靠", "实现"]
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


def re_task(path):
    def_relation = ["包含", "等价", "来源", "属于", "由组成", "实现", "被定义为", "内容", "英文名", "目标", "作用", "特点", "方法", "缺点", "创建时间", "创建者"]
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
                        subject = spo["head"]
                        object = spo["tail"]
                        input = instruction["input"]
                        datas.append([input, subject, relation, object])
                    except TypeError as e:
                        print(e)
                        print(spo)
                    except KeyError as e:
                        print(e)
                        print(spo)
    datas = pd.DataFrame(datas, columns=["input", "subject", "relation", "object"])
    datas.to_csv("RE-1.csv", index=False, encoding="utf_8_sig")

if __name__ == '__main__':
    path = "../Baichuan2-7B-RE-1_output.json"
    re_task(path)