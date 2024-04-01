## 目录结构

```
dataset
├───pdf				//知识图谱书知识点pdf版本
├───txt				//知识图谱书知识点txt版本
├───txt				//知识图谱书知识点json版本
├───ft_spo_json			//第一次微调大语言模型（SPO）的数据集原始版本
├───spo_train_data		//第一次微调大语言模型（SPO）的数据集训练版本
├───ft_re_csv			//第二次微调大语言模型（SPO）的数据集csv版本
├───spo_train_data_2	//第二次微调大语言模型（SPO）的数据集训练版本
├───utils			//版本转换工具
│	├───csv2json.py		//将数据集从csv转换成json格式
│	├───pdf2txt.py		//将书pdf转化成txt
│	├───regular_extract.py		//将txt将规范化
├───ie2instruction		//Deepke提供的转换训练数据工具，将json转换为用于训练的json
├───script			//脚本
│	├───convert.sh		//提供脚本运行Deepke的工具
```
