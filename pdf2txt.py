import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# 打开PDF文件
filename = '第一章'
pdf_filename = filename + '.pdf'
txt_filename = filename + '.txt'
pdf_path = os.path.join('dataset', 'pdf', pdf_filename)
save_path = os.path.join('dataset', 'txt')
if not os.path.exists(save_path):
    os.makedirs(save_path)
txt_path = os.path.join(save_path, txt_filename)

with open(pdf_path, 'rb') as file, open(txt_path, 'w', encoding='utf-8') as txt:
    resource_manager = PDFResourceManager()
    output = TextConverter(resource_manager, txt, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, output)

    # 逐页解析文档
    for page in PDFPage.get_pages(file):
        interpreter.process_page(page)

