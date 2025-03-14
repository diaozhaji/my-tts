#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import unicodedata
from tqdm import tqdm
import chardet

# ================= 配置区域 =================
INPUT_FILE = "txt/rbq1-70.txt"         # 输入文件路径
OUTPUT_DIR = "cleaned_chapters"     # 输出目录
ENCODING = "auto"                   # 文件编码（auto为自动检测）
KEEP_PUNCTUATION = True             # 是否保留中文标点
CHAPTER_PATTERN = re.compile(
    r'(?:^|\n)\s*((?:第[零一二三四五六七八九十百千万\d]+[章节卷集部篇][^\n]*)'  # 基础中文格式
    r'|(?:【[^】]*】)'                          # 方括号标题
    r'|(?:\d{1,3}(?:\.\d{1,3})*\.?\s*[\u4e00-\u9fa5A-Za-z0-9_\-—（）()\s]+)'  # 多级数字编号
    r'|(?:[（(][零一二三四五六七八九十百千万\d]+[）)][^\n]*)'  # 括号数字编号
    r'|(?:[【〈《*\-]\s*.*?\s*[】〉》*\-])'       # 特殊符号包裹标题
    r'|(?:[序终结跋附][幕章篇]?[^\n]*)'          # 特殊章节标识
    r'|(?:(?:卷|部|篇)\s*\d+[^\n]*)'            # 卷/部/篇+数字
    r'|(?:[上下]半部\s*[\u4e00-\u9fa5]+))'      # 上下部标识
)
# ============================================

def detect_file_encoding(file_path):
    """自动检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))
    return result['encoding'] if result['confidence'] > 0.7 else 'utf-8'

def clean_text(text):
    """优化后的文本清洗"""
    cleaned = unicodedata.normalize('NFKC', text)
    
    # 保留换行符的空白处理
    cleaned = re.sub(r'[^\S\n]+', ' ', cleaned)  # 合并非换行空白
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned) # 保留段落结构
    
    # 标点处理
    if not KEEP_PUNCTUATION:
        cleaned = re.sub(r'[，。！？、；：“”‘’（）【】《》…—]', '', cleaned)
    return cleaned.strip()

def split_chapters(text):
    """增强的章节分割"""
    # 插入分割标记并保留换行
    marked = CHAPTER_PATTERN.sub(r'\n\033CHAPTER_SPLIT\033\n\g<1>', text)
    
    chapters = []
    for chunk in marked.split('\033CHAPTER_SPLIT\033'):
        chunk = chunk.strip()
        if chunk:
            title_match = CHAPTER_PATTERN.search(chunk)
            header = title_match.group(1).strip() if title_match else ""
            content = re.sub(r'^\s*' + re.escape(header) + r'\s*', '', chunk, flags=re.MULTILINE).strip()
            chapters.append((header, content))
    return chapters

def process_novel():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 检测编码
    file_encoding = detect_file_encoding(INPUT_FILE) if ENCODING == "auto" else ENCODING
    
    try:
        with open(INPUT_FILE, 'r', encoding=file_encoding, errors='replace') as f:
            raw_text = f.read()
    except UnicodeDecodeError:
        sys.exit(f"解码失败！请尝试手动指定编码（当前检测到：{file_encoding}）")

    # cleaned = clean_text(raw_text)
    chapters = split_chapters(raw_text)
    
    print(f"正在生成 {len(chapters)} 个章节文件：")
    for idx, (title, content) in enumerate(tqdm(chapters, ncols=80), 1):
        # 生成更安全的文件名
        if title:
            clean_title = re.sub(r'\s+', ' ', re.sub(r'[\\/*?:"<>|]', '_', title))
            filename = f"{clean_title}.txt"
        else:
            filename = f"chapter_{idx:04d}.txt"
        
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{content}")

    print(f"处理完成！输出目录：{os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    process_novel()