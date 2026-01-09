#!/usr/bin/env python3
"""
Скрипт для переименования всех файлов и папок с кириллицы на английский
"""
import os
import re
from pathlib import Path
import shutil

# Маппинг русских названий на английские
TRANSLATIONS = {
    # Папки
    '00_introduction': '00_introduction',
    '01_chapter_01': '01_chapter_01',
    '02_chapter_02': '02_chapter_02',
    '03_chapter_03': '03_chapter_03',
    '04_chapter_04': '04_chapter_04',
    '05_chapter_05': '05_chapter_05',
    '06_chapter_06': '06_chapter_06',
    '07_chapter_07': '07_chapter_07',
    '08_chapter_08': '08_chapter_08',
    '09_chapter_09': '09_chapter_09',
    '10_chapter_10': '10_chapter_10',
    '11_chapter_11': '11_chapter_11',
    '12_chapter_12': '12_chapter_12',
    '13_conclusion': '13_conclusion',
    
    # Файлы введения
    '01_цель_и_задачи_книги': '01_goals_and_objectives',
    '02_обзор_современного_состояния': '02_current_state_overview',
    '03_структура_и_методология': '03_structure_and_methodology',
    
    # Глава 1
    '01_понятие_ии_и_мл': '01_ai_and_ml_concepts',
    '02_типы_алгоритмов_мл': '02_ml_algorithm_types',
    '03_нейронные_сети': '03_neural_networks',
    '04_особенности_применения_ии': '04_ai_application_features',
    '05_преимущества_и_ограничения': '05_advantages_and_limitations',
    
    # Глава 2
    '01_типы_геологических_данных': '01_geological_data_types',
    '02_проблемы_качества_данных': '02_data_quality_issues',
    '03_интеграция_разнородных_данных': '03_heterogeneous_data_integration',
    '04_предобработка_и_нормализация': '04_preprocessing_and_normalization',
    '05_пространственно_временные_данные': '05_spatiotemporal_data',
    
    # Глава 3
    '01_традиционные_подходы_гис': '01_traditional_well_logging_approaches',
    '02_мл_для_литологической_типизации': '02_ml_for_lithological_typing',
    '03_определение_коллекторских_свойств': '03_reservoir_properties_determination',
    '04_прогнозирование_пористости': '04_porosity_prediction',
    '05_выделение_продуктивных_интервалов': '05_productive_intervals_identification',
    '06_кейс_стади_гис': '06_case_study_well_logging',
    
    # Глава 4
    '01_цифровой_анализ_керна': '01_digital_core_analysis',
    '02_компьютерное_зрение_керн': '02_computer_vision_core',
    '03_определение_литотипа': '03_lithotype_determination',
    '04_томография_керна': '04_core_tomography',
    '05_интеграция_керн_каротаж': '05_core_logging_integration',
    '06_прогнозирование_фэс': '06_fecs_prediction',
    
    # Глава 5
    '01_классификация_пород_коллекторов': '01_reservoir_rock_classification',
    '02_электролипы_и_фациальный_анализ': '02_electrofacies_and_facies_analysis',
    '03_петрофизические_зависимости': '03_petrophysical_relationships',
    '04_насыщенность_флюидами': '04_fluid_saturation',
    '05_механические_свойства_пород': '05_rock_mechanical_properties',
    '06_оценка_неопределенностей': '06_uncertainty_assessment',
    
    # Глава 6
    '01_автоматическая_интерпретация_сейсмики': '01_automatic_seismic_interpretation',
    '02_глубокое_обучение_сейсмограммы': '02_deep_learning_seismograms',
    '03_выделение_геологических_структур': '03_geological_structures_identification',
    '04_прогнозирование_залежей': '04_deposits_prediction',
    '05_снижение_дисперсии': '05_dispersion_reduction',
    '06_интеграция_сейсмика_скважины': '06_seismic_well_integration',
    
    # Глава 7
    '01_автоматизация_геологических_карт': '01_geological_maps_automation',
    '02_анализ_спутниковых_снимков': '02_satellite_imagery_analysis',
    '03_классификация_пород_по_спектрам': '03_rock_spectral_classification',
    '04_выявление_аномалий': '04_anomalies_detection',
    '05_мониторинг_ландшафта': '05_landscape_monitoring',
    '06_гиперспектральные_данные': '06_hyperspectral_data',
    
    # Глава 8
    '01_ии_в_нефтегазовой_геологии': '01_ai_in_oil_gas_geology',
    '02_прогнозирование_продуктивности': '02_productivity_prediction',
    '03_оптимизация_размещения_скважин': '03_well_placement_optimization',
    '04_анализ_геохимических_данных': '04_geochemical_data_analysis',
    '05_3d_геологические_модели': '05_3d_geological_models',
    '06_оценка_перспективности': '06_prospectivity_assessment',
    
    # Глава 9
    '01_обзор_программных_пакетов': '01_software_packages_overview',
    '02_python_и_библиотеки': '02_python_and_libraries',
    '03_облачные_вычисления': '03_cloud_computing',
    '04_интеграция_с_гис_сапр': '04_gis_cad_integration',
    '05_разработка_алгоритмов': '05_algorithm_development',
    
    # Глава 10
    '01_специфика_big_data': '01_big_data_specifics',
    '02_хранение_и_управление_данными': '02_data_storage_and_management',
    '03_параллельные_вычисления': '03_parallel_computing',
    '04_потоковый_анализ': '04_streaming_analysis',
    '05_оптимизация_производительности': '05_performance_optimization',
    
    # Глава 11
    '01_цифровизация_процессов': '01_process_digitalization',
    '02_автоматизация_западная_сибирь': '02_automation_west_siberia',
    '03_ии_в_карбонатных_коллекторах': '03_ai_in_carbonate_reservoirs',
    '04_поиск_пропущенных_залежей': '04_missed_deposits_search',
    '05_оптимизация_доразведки': '05_appraisal_optimization',
    
    # Глава 12
    '01_метрики_оценки_качества': '01_quality_metrics',
    '02_сравнение_с_традиционными_методами': '02_traditional_methods_comparison',
    '03_экономическая_эффективность': '03_economic_efficiency',
    '04_анализ_рисков': '04_risk_analysis',
    '05_временные_преимущества': '05_time_advantages',
    
    # Заключение
    '01_основные_достижения': '01_main_achievements',
    '02_рекомендации_по_внедрению': '02_implementation_recommendations',
    '03_направления_исследований': '03_research_directions',
    '04_прогноз_развития': '04_development_forecast',
}

# Обратный маппинг для обновления ссылок
REVERSE_TRANSLATIONS = {v: k for k, v in TRANSLATIONS.items()}

def get_english_name(russian_name):
    """Получает английское имя из русского"""
    # Убираем расширение
    base_name = russian_name.replace('.md', '')
    
    # Проверяем в маппинге
    if base_name in TRANSLATIONS:
        return TRANSLATIONS[base_name] + ('.md' if russian_name.endswith('.md') else '')
    
    # Если не найдено, возвращаем как есть
    return russian_name

def rename_files_and_folders():
    """Переименовывает все файлы и папки"""
    renamed = []
    
    # Сначала переименовываем файлы
    for root, dirs, files in os.walk('.'):
        # Пропускаем служебные директории
        if any(skip in root for skip in ['.git', '_site', 'node_modules', '.github', '__pycache__']):
            continue
        
        for file in files:
            if file.endswith('.md') and not file.startswith('README'):
                file_path = Path(root) / file
                base_name = file.replace('.md', '')
                
                if base_name in TRANSLATIONS:
                    new_name = TRANSLATIONS[base_name] + '.md'
                    new_path = file_path.parent / new_name
                    
                    if file_path.exists() and file_path != new_path:
                        shutil.move(str(file_path), str(new_path))
                        renamed.append((str(file_path), str(new_path)))
                        print(f"Renamed: {file_path} -> {new_path}")
    
    return renamed

def update_links_in_file(file_path, translations):
    """Обновляет ссылки в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Обновляем ссылки на файлы
        for russian, english in translations.items():
            # Паттерны для поиска ссылок
            patterns = [
                (f'{russian}.md', f'{english}.md'),
                (f'{russian}.html', f'{english}.html'),
                (f'/{russian}/', f'/{english}/'),
                (f'/{russian}.', f'/{english}.'),
            ]
            
            for old_pattern, new_pattern in patterns:
                content = content.replace(old_pattern, new_pattern)
        
        # Если были изменения, сохраняем
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated links in: {file_path}")
            return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
    
    return False

def main():
    print("Renaming files from Cyrillic to English...")
    print("=" * 50)
    
    # Переименовываем файлы
    renamed = rename_files_and_folders()
    
    print("\n" + "=" * 50)
    print("Updating links in HTML and Markdown files...")
    
    # Обновляем ссылки в файлах
    files_to_update = [
        'index.html',
        '_layouts/default.html',
        '_config.yml',
    ]
    
    # Также обновляем все markdown файлы
    for root, dirs, files in os.walk('.'):
        if any(skip in root for skip in ['.git', '_site', 'node_modules', '.github']):
            continue
        
        for file in files:
            if file.endswith(('.md', '.html', '.yml')):
                file_path = Path(root) / file
                if file_path.name not in ['README.md', 'DEPLOY.md', 'add_front_matter.py', 'rename_to_english.py']:
                    update_links_in_file(file_path, TRANSLATIONS)
    
    print("\n" + "=" * 50)
    print(f"Done! Renamed {len(renamed)} files.")
    print("\nPlease review the changes and test the site locally if possible.")

if __name__ == '__main__':
    main()

