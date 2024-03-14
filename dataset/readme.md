# 构建微调数据集

需要构建一个微调数据集来在知识工程专业领域上对我们的模型进行微调。

⚠️请使用[format_txt文件夹](./format_txt/)中的句子完成微调数据集。

需要1000+以上的数据进行微调，因此每章需要100+以上条语句数据

分工：愿篠1，Lu23，夜壶45，祓晓67，吉祥物89

`head_type`和`tail_type`分为两种：**概念**和**产品**，产品就是开发出来的工具应用软件等等，其他都算概念。同时检查一下所有被引号框起来的文本中不能有空格，把空格删了或者对于英文短语空格用下划线替换
## 抽取三元组

首先抽取句子中的三元组信息

格式：（head_type和tail_type请暂时置为空）

```
{"text": "...", "relation": [{"head": "...", "head_type": "", "relation": "...", "tail": "...", "tail_type": " "}, {"head": "...", "head_type": " ", "relation": "...", "tail": "...", "tail_type": " "}, ...]}
```

例如对于这样一句话

```
{"text": "知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]。"}
```

中存在一个三元关系：知识图谱 是 技术方法

那么该语句构建的数据集为

```
{"text": "知识图谱是一种用图模型来描述知识和建模世界万物之间的关联关系的技术方法[1]。", "relation": [{"head": "知识图谱", "head_type": "", "relation": "属于", "tail": "技术方法", "tail_type": ""}]}
```

⚠️⚠️更具体可以参考[SPO文件夹](../DeepKE/example/llm/InstructKGC/data/SPO)中[sample.json](../DeepKE/example/llm/InstructKGC/data/SPO/sample.json)的格式（head_type和tail_type请暂时置为空）
