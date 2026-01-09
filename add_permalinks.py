#!/usr/bin/env python3
"""
Скрипт для добавления permalinks ко всем markdown файлам
"""
import os
import re
from pathlib import Path

def get_permalink(file_path):
    """Генерирует permalink для файла"""
    # Получаем относительный путь от корня
    rel_path = str(file_path).replace('\\', '/')
    
    # Убираем расширение .md
    permalink = rel_path.replace('.md', '.html')
    
    # Убираем ведущий ./ если есть
    if permalink.startswith('./'):
        permalink = permalink[2:]
    
    return f"/{permalink}"

def add_permalink_to_file(file_path):
    """Добавляет permalink к front matter файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, есть ли front matter
        if not content.startswith('---'):
            print(f"[SKIP] {file_path} - no front matter")
            return False
        
        # Извлекаем front matter
        front_matter_end = content.find('---', 3)
        if front_matter_end == -1:
            print(f"[SKIP] {file_path} - invalid front matter")
            return False
        
        front_matter = content[3:front_matter_end].strip()
        body = content[front_matter_end + 3:].lstrip()
        
        # Проверяем, есть ли уже permalink
        if 'permalink:' in front_matter:
            print(f"[SKIP] {file_path} - already has permalink")
            return False
        
        # Добавляем permalink
        permalink = get_permalink(file_path)
        front_matter += f"\npermalink: {permalink}"
        
        # Собираем обратно
        new_content = f"---\n{front_matter}\n---\n{body}"
        
        # Сохраняем
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[OK] Added permalink to {file_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def process_directory(directory):
    """Обрабатывает все markdown файлы в директории"""
    count = 0
    for root, dirs, files in os.walk(directory):
        # Пропускаем служебные директории
        if any(skip in root for skip in ['.git', '_site', 'node_modules', '.github', '__pycache__']):
            continue
        
        for file in files:
            if file.endswith('.md') and file not in ['README.md', 'DEPLOY.md', 'index.md']:
                file_path = Path(root) / file
                if add_permalink_to_file(file_path):
                    count += 1
    
    return count

if __name__ == '__main__':
    print("Adding permalinks to markdown files...")
    print("=" * 50)
    count = process_directory('.')
    print("=" * 50)
    print(f"Done! Updated {count} files.")

