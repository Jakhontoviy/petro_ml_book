#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления навигации в default.html на основе реальной структуры книги
"""

import re
from pathlib import Path

def extract_title_from_file(file_path):
    """Извлекает заголовок из front matter файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем title в front matter
    title_match = re.search(r'title:\s*(.+)', content)
    if title_match:
        return title_match.group(1).strip()
    
    # Если нет title, используем имя файла
    return file_path.stem.replace('_', ' ').title()

# Словарь с короткими названиями глав
CHAPTER_NAMES = {
    1: "Основы искусственного интеллекта",
    2: "Специфика геологических данных для ИИ",
    3: "Автоматизированная интерпретация ГИС",
    4: "Анализ керна с применением ИИ",
    5: "Петрофизическое моделирование и типизация пород",
    6: "Сейсморазведка и ИИ",
    7: "Геологическое картирование и дистанционное зондирование",
    8: "Поиск и разведка месторождений",
    9: "Программные решения и платформы",
    10: "Обработка больших данных в геологии",
    11: "Кейсы применения ИИ в нефтегазовой отрасли",
    12: "Результаты и эффективность применения ИИ",
    13: "Заключение"
}

def get_chapter_structure(base_dir):
    """Получает структуру всех глав"""
    chapters = []
    
    # Введение
    intro_dir = base_dir / "00_introduction"
    if intro_dir.exists():
        intro_files = sorted(intro_dir.glob("*.md"))
        chapters.append({
            'name': 'Введение',
            'dir': '00_introduction',
            'files': [{'path': f, 'title': extract_title_from_file(f)} for f in intro_files]
        })
    
    # Главы 1-13
    for i in range(1, 14):
        chapter_num = f"{i:02d}"
        chapter_dirs = list(base_dir.glob(f"{chapter_num}_*"))
        if chapter_dirs:
            chapter_dir = chapter_dirs[0]
            chapter_files = sorted(chapter_dir.glob("*.md"))
            
            # Используем короткое название из словаря
            chapter_name = CHAPTER_NAMES.get(i, f"Глава {i}")
            if i < 13:
                chapter_name = f"Глава {i}. {chapter_name}"
            
            chapters.append({
                'name': chapter_name,
                'dir': chapter_dir.name,
                'files': [{'path': f, 'title': extract_title_from_file(f)} for f in chapter_files]
            })
    
    return chapters

def generate_navigation_html(chapters, base_url=""):
    """Генерирует HTML для навигации"""
    html_parts = []
    
    # Введение
    intro = chapters[0]
    html_parts.append('                        <li>')
    html_parts.append(f'                            <strong>{intro["name"]}</strong>')
    html_parts.append('                            <ul>')
    for file_info in intro['files']:
        file_name = file_info['path'].stem
        title = file_info['title']
        # Упрощаем заголовок для навигации
        short_title = re.sub(r'^\d+\.\d+\.\s*', '', title)
        html_parts.append(f'                                <li><a href="{{{{ \'/{intro["dir"]}/{file_name}.html\' | relative_url }}}}">{short_title}</a></li>')
    html_parts.append('                            </ul>')
    html_parts.append('                        </li>')
    
    # Группируем главы по частям
    parts = {
        'Часть I. Теоретические основы': [1, 2],
        'Часть II. Петрофизические исследования': [3, 4, 5],
        'Часть III. Геологическое моделирование': [6, 7, 8],
        'Часть IV. Инструменты и технологии': [9, 10],
        'Часть V. Практическое применение': [11, 12],
    }
    
    current_part = None
    for i, chapter in enumerate(chapters[1:], 1):
        # Определяем, к какой части относится глава
        part_name = None
        for part, chapter_nums in parts.items():
            if i in chapter_nums:
                part_name = part
                break
        
        if part_name and part_name != current_part:
            if current_part is not None:
                html_parts.append('                            </ul>')
                html_parts.append('                        </li>')
            current_part = part_name
            html_parts.append('                        <li>')
            html_parts.append(f'                            <strong>{part_name}</strong>')
            html_parts.append('                            <ul>')
        
        # Добавляем главу
        chapter_num = i
        html_parts.append(f'                                <li>')
        html_parts.append(f'                                    <strong>{chapter["name"]}</strong>')
        html_parts.append('                                    <ul>')
        for file_info in chapter['files']:
            file_name = file_info['path'].stem
            title = file_info['title']
            # Упрощаем заголовок для навигации
            short_title = re.sub(r'^\d+\.\d+\.\s*', '', title)
            html_parts.append(f'                                        <li><a href="{{{{ \'/{chapter["dir"]}/{file_name}.html\' | relative_url }}}}">{short_title}</a></li>')
        html_parts.append('                                    </ul>')
        html_parts.append('                                </li>')
    
    # Закрываем последнюю часть
    if current_part:
        html_parts.append('                            </ul>')
        html_parts.append('                        </li>')
    
    # Заключение
    conclusion = chapters[-1] if chapters[-1]['name'] == 'Заключение' else None
    if conclusion:
        html_parts.append('                        <li>')
        html_parts.append(f'                            <strong>{conclusion["name"]}</strong>')
        html_parts.append('                            <ul>')
        for file_info in conclusion['files']:
            file_name = file_info['path'].stem
            title = file_info['title']
            short_title = re.sub(r'^\d+\.\d+\.\s*', '', title)
            html_parts.append(f'                                <li><a href="{{{{ \'/{conclusion["dir"]}/{file_name}.html\' | relative_url }}}}">{short_title}</a></li>')
        html_parts.append('                            </ul>')
        html_parts.append('                        </li>')
    
    return '\n'.join(html_parts)

def update_navigation():
    """Обновляет навигацию в default.html"""
    base_dir = Path(__file__).parent
    layout_file = base_dir / "_layouts" / "default.html"
    
    print("Обновление навигации...")
    print(f"Базовый каталог: {base_dir}")
    
    # Получаем структуру глав
    chapters = get_chapter_structure(base_dir)
    print(f"\nНайдено глав: {len(chapters)}")
    
    # Генерируем HTML навигации
    nav_html = generate_navigation_html(chapters)
    
    # Читаем текущий layout
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим и заменяем навигацию
    # Ищем блок с навигацией (между <nav class="chapter-nav"> и </nav>)
    pattern = r'(<nav class="chapter-nav">\s*<h3>Навигация</h3>\s*<ul>)(.*?)(</ul>\s*</nav>)'
    
    replacement = f'\\1\n                        <li><a href="{{{{ \'/\' | relative_url }}}}">Содержание</a></li>\n{nav_html}\n                    \\3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(layout_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n[OK] Навигация обновлена в: {layout_file}")
        print(f"     Добавлено глав: {len(chapters)}")
        print(f"     Всего разделов: {sum(len(ch['files']) for ch in chapters)}")
    else:
        print("\n[INFO] Навигация не изменилась или не найдена")

if __name__ == "__main__":
    update_navigation()
