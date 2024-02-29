## 目录结构

```
root
│   pdf2txt.py
│		
├───dataset
│       ├───pdf
│				    	第一章.pdf
│						  ...
│       ├───txt
│       		  第一章.txt
│       			...
│
```

## 环境

```
```

## 步骤

1. 安装pdfminer

```
pip install pdfminer.six
pip3 install pdfminer3k
```

2. 首先在`./dataset/pdf/知识图谱方法、实践及应用_副本.pdf`中导出所需章节，修改pdf2txt.py中filename，运行pdf2txt.py，可以在``./dataset/txt`中获得纯文本格式
3. 