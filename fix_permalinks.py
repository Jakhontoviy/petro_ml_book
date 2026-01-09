#!/usr/bin/env python3
"""
Скрипт для обновления permalinks с учетом baseurl
"""
import os
import re
from pathlib import Path

BASEURL = "/petro_ml_book"

def update_permalink_in_file(file_path):
    """Обновляет permalink в файле с учетом baseurl"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return False
        
        # Извлекаем front matter
        front_matter_end = content.find('---', 3)
        if front_matter_end == -1:
            return False
        
        front_matter = content[3:front_matter_end].strip()
        body = content[front_matter_end + 3:].lstrip()
        
        # Получаем текущий permalink
        permalink_match = re.search(r'permalink:\s*(.+)', front_matter)
        if not permalink_match:
            return False
        
        current_permalink = permalink_match.group(1).strip()
        
        # Если permalink уже содержит baseurl, пропускаем
        if BASEURL in current_permalink:
            return False
        
        # Обновляем permalink
        # Убираем ведущий слэш если есть
        if current_permalink.startswith('/'):
            new_permalink = BASEURL + current_permalink
        else:
            new_permalink = BASEURL + '/' + current_permalink
        
        # Заменяем в front matter
        new_front_matter = re.sub(
            r'permalink:\s*.+',
            f'permalink: {new_permalink}',
            front_matter
        )
        
        # Собираем обратно
        new_content = f"---\n{new_front_matter}\n---\n{body}"
        
        # Сохраняем
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[OK] Updated permalink in {file_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def process_directory(directory):
    """Обрабатывает все markdown файлы"""
    count = 0
    for root, dirs, files in os.walk(directory):
        if any(skip in root for skip in ['.git', '_site', 'node_modules', '.github', '__pycache__']):
            continue
        
        for file in files:
            if file.endswith('.md') and file not in ['README.md', 'DEPLOY.md', 'index.md', 'TROUBLESHOOTING.md']:
                file_path = Path(root) / file
                if update_permalink_in_file(file_path):
                    count += 1
    
    return count

if __name__ == '__main__':
    print(f"Updating permalinks with baseurl: {BASEURL}")
    print("=" * 50)
    count = process_directory('.')
    print("=" * 50)
    print(f"Done! Updated {count} files.")

