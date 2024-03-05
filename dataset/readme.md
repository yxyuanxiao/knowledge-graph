# 构建微调数据集

需要构建一个微调数据集来在知识工程专业领域上对我们的模型进行微调

## NER微调数据集

首先需要定义一些类（参考上学期实验一中定义的 Class），比如

```
"人物", "地理位置", "组织机构" ...
```

需要大家商量一下，找出所有的类，然后对于每个类，在每章里面找到5句话，这些句子中带有这个实例

比如我定义知识工程中知识点中的类：术语，项目（我暂时想到两个，还需要补充/细分），对于这样几句话

```
1. 知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]。
2. 例如，WordNet[23]是典型的语义网络，它定义了名词、 动词、形容词和副词之间的语义关系。
```

他们构建的NER数据集是这样

把类放入schema.json文件

```
["术语", "项目"]
```

对于每个句子，放入sample.json文件

```
{"text": "知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]", "entity": [{"entity": "知识图谱", "entity_type": "术语"}, {"entity": "技术方法", "entity_type": "术语"}]}
{"text": "例如，WordNet[23]是典型的语义网络，它定义了名词、 动词、形容词和副词之间的语义关系。", "entity": [{"entity": "WordNet", "entity_type": "项目"}, {"entity": "语义网络", "entity_type": "术语"}]}
```

⚠️⚠️请务必参考[NER文件夹](../DeepKE/example/llm/InstructKGC/data/NER)中[sample.json](../DeepKE/example/llm/InstructKGC/data/NER/sample.json)和[schema.json](../DeepKE/example/llm/InstructKGC/data/NER/schema.json)的格式

## RE微调数据集

同NER一样，需要定义一些关系名，比如

```
"创始人","出生日期","作者"...
```

找出所有的关系，然后对于每个关系，在每章里面找到5句话，这些句子中带有这个关系

比如我定义 **属于** 关系，对于

```
知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]。
```

构建的RE数据集是这样

把关系名放入schema.json文件

```
["属于"]
```

对于每个句子，放入sample.json文件

```
{"text": "知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]。", "relation": [{"head": "知识图谱", "relation": "属于", "tail": "技术方法"}]}
```

⚠️⚠️请务必参考[NER文件夹](../DeepKE/example/llm/InstructKGC/data/RE)中[sample.json](../DeepKE/example/llm/InstructKGC/data/RE/sample.json)和[schema.json](../DeepKE/example/llm/InstructKGC/data/RE/schema.json)的格式