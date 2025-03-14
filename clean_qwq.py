import re

def clean_text(text):
    """去除特殊字符，保留中文、英文、数字和常见标点"""
    # 保留中文、英文、数字、空格和常见的标点符号（如.,!?等）
    cleaned = re.sub(r'[^\w\s,.!?;:()\'"-]+', ' ', text)
    # 去除多余空格并替换换行符
    return re.sub(r'\s+', ' ', cleaned).replace('\n', '\n')

def split_chapters(text):
    """分割章节，返回章节标题和内容的字典列表"""
    chapters = []
    current_title = None
    current_content = ""
    
    # 章节标题模式（匹配"第五章"或"5."等形式）
    pattern = r'^\s*(?:第\s*\d+\s*[章]|^\d+\.)'
    
    for line in text.split('\n'):
        stripped_line = line.strip()
        
        # 检查是否是章节标题
        if re.match(pattern, stripped_line):
            if current_title is not None:
                chapters.append({'title': current_title, 'content': current_content})
                current_content = ""
            current_title = stripped_line
        else:
            current_content += line + '\n'
    
    # 添加最后一个章节（如果存在）
    if current_title and current_content.strip():
        chapters.append({'title': current_title, 'content': current_content})
        
    return chapters

def save_chapters(chapters):
    """保存每个章节为单独的文本文件"""
    for idx, chapter in enumerate(chapters):
        filename = f"chapter_{idx+1}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            content = clean_text(chapter['content'])
            f.write(f"{chapter['title']}\n{content}")
        print(f"Saved: {filename}")

if __name__ == "__main__":
    input_path = 'txt/byn.txt'  # 小说文件路径
    try:
        with open(input_path, "r", encoding="utf-8",errors="ignore") as file:
            text = file.read()
            
        cleaned_text = clean_text(text)
        chapters = split_chapters(cleaned_text)
        
        if len(chapters) > 0:
            save_chapters(chapters)
        else:
            print("章节分割失败，请检查文本格式是否包含有效的章节标题")
    except Exception as e:
        print(f"Error: {e}")
