import json
import re

pattern = re.compile('([^。]+。)')  # 定义正则表达式
pattern_title = re.compile('(图\\d+-\\d+)')


def extract_sentences_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:  # 报错了换成 with open(file_path, 'r', encoding='gbk') as f:
        text = f.read()  # 读取文件内容
    sentences = pattern.findall(text)  # 使用正则表达式提取句子
    return sentences


def save_sentences_to_file(sentences, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            # f.write('{"text":"%s"}\n\n' % sentence)  # 写入句子并留有空行
            # sentence = sentence.strip()  # 去除句子两侧的空白字符（包括换行符）
            if not pattern_title.match(sentence):
                sentence = sentence.replace('\n', '').replace('\f', '')  # 去除特殊字符
                sentence_json = json.dumps({"text": sentence}, ensure_ascii=False)  # 将句子转换为JSON字符串
                f.write(sentence_json + '\n')  # 写入句子并留有空行


# 示例用法
file_path = 'path\\name.txt'  # 替换为实际的文件路径
output_file = 'name.json'  # 替换为实际的输出文件路径

sentences = extract_sentences_from_file(file_path)
save_sentences_to_file(sentences, output_file)
