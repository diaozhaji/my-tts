import os
import re
import chardet

def clean_text(text):
    # 去掉全角的数字和字母，并将其转换为半角
    cleaned_text = re.sub(r'[\uFF10-\uFF19\uFF21-\uFF3A\uFF41-\uFF5A]', lambda m: chr(ord(m.group()) - 65248), text)
    return cleaned_text

def split_into_chapters(file_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
    
    with open(file_path, 'r', encoding=detected_encoding, errors='ignore') as file:
        text = file.read()
    
    cleaned_text = clean_text(text)
    
    # 匹配章节标记的正则表达式，覆盖更多的模式
    chapter_pattern = re.compile(r'(Chapter\s*\d+|第\d+章|^\s*[\u4e00-\u9fff]+\s*$)', re.MULTILINE)
    chapters = chapter_pattern.split(cleaned_text)
    
    # 去掉空的章节和开头多余的空格
    chapters = [chapter.strip() for chapter in chapters if chapter.strip()]
    
    # 将每个章节保存到单独的文件中
    for index, chapter in enumerate(chapters):
        if chapter:
            output_file_path = f"{output_dir}/chapter_{index + 1}.txt"
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(chapter)

if __name__ == "__main__":
    file_path = 'txt/ysys.txt'  # 小说文件路径
    output_dir = 'chapters'  # 输出目录
    
    split_into_chapters(file_path, output_dir)
