import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

filenames = ["第一章", "第二章", "第三章", "第四章", "第五章", "第六章", "第七章", "第八章", "第九章"]
# 打开PDF文件
for filename in filenames:
    pdf_filename = filename + '.pdf'
    txt_filename = filename + '1.txt'
    pdf_path = os.path.join('../', 'pdf', pdf_filename)
    save_path = os.path.join('../', 'txt')
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

