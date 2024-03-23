# 标注任务

yx1 lu2 cyl3 htz6 txy8

每章节100行标注语句

1. 对于标注的语句检查其是否是可以提取到知识点的
2. 检查其subject和object是否正确
3. 根据Schema标注subject_type和object_type
4. 根据Schema标注subject和object的关系

有感觉可以通用的relation再补充schema

**最后标注的语句的subject、object、subject_type和object_type应该都有，而没标注的的这些都是空的**

选做：对于未标注的句子删除无用语句，检查其subject和object是否正确

## Schema

### 实体 Schema

```
知识图谱
知识表示
知识存储
知识抽取
知识融合
知识推理
语义搜索
知识问答
知识图谱项目
```

### Relation Schema

#### 实体之间的relation

```
包含
等价
来源
属于
由组成
```

#### 属性relation

```
实体_被定义为_文本
实体_内容_文本
实体_英文名_文本
实体_目标_文本
实体_作用_文本
实体_特点_文本
实体_方法_文本
知识图谱项目_创建时间_时间
知识图谱项目_创建者_人物/实验室
```

## 