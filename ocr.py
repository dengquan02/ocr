# 导入库
import io
from tqdm import tqdm
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import os

# 设置路径
poppler_path = r'D:\Program Files\ocr\poppler-23.08.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\ocr\Tesseract-OCR\tesseract.exe'

# 文件夹路径
read_folder_path = r"D:\Documents\ocr\pdf"
write_folder_path = r"D:\Documents\ocr\finished"

def convert(PDF_file_Read, PDF_file_Writer):
    # 将所有的PDF页面转换为图像对象
    print('将所有的PDF页面转换为图像对象...')
    images = convert_from_path(PDF_file_Read, poppler_path=poppler_path)

    # 创建一个PDF写入对象
    print('创建一个PDF写入对象...')
    pdf_writer = PyPDF2.PdfWriter()

    # 遍历每个图像对象
    print('遍历每个图像对象...')
    for image in tqdm(images):
        # 将图像转换为可搜索的PDF页面
        page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='chi_sim')
        # 创建一个PDF读取对象
        pdf = PyPDF2.PdfReader(io.BytesIO(page))
        # 将页面添加到PDF写入对象中
        pdf_writer.add_page(pdf.pages[0])

    # 导出可搜索的PDF文件
    print('导出可搜索的PDF文件...')
    with open(PDF_file_Writer, "wb") as f:
        pdf_writer.write(f)
    print('Done!')


# 列出目录下的所有文件和文件夹
file_list = os.listdir(read_folder_path)

for file_name in file_list:
    # 拼接目录名和文件名
    read_path = os.path.join(read_folder_path, file_name)
    write_path = os.path.join(write_folder_path, file_name)
    print(read_path, write_path)

    # 判断是否为文件
    if os.path.isfile(read_path):
        # 进行相应处理
        convert(read_path, write_path)

print('finally successful!')