# 知识工程课程知识图谱构建与应用

## 目录结构

```
root
├───requirements.txt
│
├───dataset				//训练数据
├───output				//模型输出
│
├───DeepKE
│	├───bert-base-chinese
│		...
```

## 环境

```
pdfminer3k==1.3.4
```

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

## 步骤

### 配置环境

1. 下载基本代码

```
git clone https://github.com/yxyuanxiao/knowledge-graph.git
```

2. 使用`Anaconda`创建一个虚拟环境
```
conda create -n deepke python=3.8

conda activate deepke
```


3. 安装pdfminer

```
pip install pdfminer.six
pip3 install pdfminer3k
```

4. 进入`DeepKE`目录

```
cd ./knowledge-graph/DeepKE/
```

5. 安装DeepKE

```
pip install -r requirements.txt
python setup.py install
python setup.py develop
```

6. 下载[bert-base-chinese](https://huggingface.co/google-bert/bert-base-chinese/tree/main)，至少下载`config.json, pytorch_model.bin, tokenizer.json, tokenizer_config.json, vocab.txt`，将五个文件放入一个`bert-base-chinese`文件夹中，将`bert-base-chinese`放入`DeepKE`中，保证文件结构为

```
root
├───DeepKE
│	├───bert-base-chinese
│		├───config.json
│		├───pytorch_model.bin
│		├───tokenizer.json
│		├───tokenizer_config.json
│		├───vocab.txt
```

7. 设置模型路径。打开文件`/knowledge-graph/DeepKE/example/ner/standard/conf/hydra/model/bert.yaml`，将`bert_model`参数改成`bert-base-chinese`的**绝对路径**，打开文件`/knowledge-graph/DeepKE/example/re/standard/conf/model/lm.yaml` ，将`lm_file`参数改成`bert-base-chinese`的**绝对路径**

⚠️⚠️RTX3090及以上显卡会出现的问题：

遇到如下报错

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
```

请在终端中输入

```
python
import torch; print(torch.cuda.get_device_capability())
```

若出现如下警告

```
NVIDIA GeForce RTX 3090 with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3090 GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/
```

则是显卡的算力太高而pytroch的版本太低，则需要卸载pytorch重新安装新版本

```
pip uninstall torch
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 测试环境

1. 输入任务目录

```
cd DeepKE/example/re/standard
```

2. 下载数据集

```
wget 120.27.214.45/Data/re/standard/data.tar.gz
tar -xzvf data.tar.gz
```

3. 训练

```
python run.py
```
