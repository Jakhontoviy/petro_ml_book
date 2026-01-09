#!/usr/bin/env python3
"""
Скрипт для добавления Jekyll front matter к markdown файлам
"""
import os
import re
from pathlib import Path

def get_title_from_filename(filename):
    """Извлекает заголовок из имени файла"""
    # Убираем расширение и префикс с номером
    name = filename.replace('.md', '')
    # Убираем начальные цифры и подчеркивания
    name = re.sub(r'^\d+_', '', name)
    # Заменяем подчеркивания на пробелы
    name = name.replace('_', ' ')
    # Делаем первую букву заголовка заглавной
    return name.capitalize()

def add_front_matter(file_path):
    """Добавляет front matter к файлу, если его еще нет"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже front matter
    if content.startswith('---'):
        print(f"[OK] {file_path} already has front matter")
        return
    
    # Получаем заголовок из первого заголовка markdown или из имени файла
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = get_title_from_filename(file_path.name)
    
    # Создаем front matter
    front_matter = f"""---
layout: default
title: {title}
---

"""
    
    # Добавляем front matter к содержимому
    new_content = front_matter + content
    
    # Сохраняем файл
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] Added front matter to {file_path}")

def process_directory(directory):
    """Обрабатывает все markdown файлы в директории"""
    for root, dirs, files in os.walk(directory):
        # Пропускаем служебные директории
        if any(skip in root for skip in ['.git', '_site', 'node_modules']):
            continue
        
        for file in files:
            if file.endswith('.md') and file != 'README.md' and file != 'index.md':
                file_path = Path(root) / file
                add_front_matter(file_path)

if __name__ == '__main__':
    print("Adding Jekyll front matter to markdown files...")
    process_directory('.')
    print("\nDone!")

