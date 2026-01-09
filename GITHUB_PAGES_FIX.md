# Исправление проблемы с GitHub Pages

## Что было исправлено:

1. ✅ Добавлен правильный `baseurl: "/petro_ml_book"` в `_config.yml`
2. ✅ Обновлены все permalinks (убраны baseurl, так как Jekyll добавляет его автоматически)
3. ✅ Настроены defaults для всех папок
4. ✅ Добавлены include директории

## Что нужно сделать:

### 1. Закоммитьте и запушьте изменения:

```bash
git add .
git commit -m "Fix: Configure baseurl and permalinks for GitHub Pages"
git push
```

### 2. Проверьте настройки GitHub Pages:

1. Перейдите в **Settings** → **Pages**
2. Убедитесь, что:
   - **Source**: ветка `main` (или `master`)
   - **Folder**: `/ (root)`
   - **Custom domain**: пусто (если не используете)

### 3. Дождитесь сборки:

1. Перейдите в раздел **Actions**
2. Дождитесь завершения workflow "Deploy GitHub Pages"
3. Проверьте, что сборка прошла успешно (зеленый статус)

### 4. Проверьте URL:

После успешной сборки страница должна быть доступна по адресу:
```
https://jakhontoviy.github.io/petro_ml_book/00_introduction/01_goals_and_objectives.html
```

## Если страница все еще не работает:

### Вариант 1: Проверьте логи сборки

1. В разделе **Actions** откройте последний workflow run
2. Проверьте логи на наличие ошибок
3. Обратите внимание на ошибки типа:
   - "Liquid Exception"
   - "Invalid YAML"
   - "Layout not found"

### Вариант 2: Проверьте локально

Запустите локально для проверки:

```bash
bundle install
bundle exec jekyll serve --baseurl /petro_ml_book
```

Откройте http://localhost:4000/petro_ml_book/00_introduction/01_goals_and_objectives.html

### Вариант 3: Альтернативное решение - использовать _pages

Если файлы все еще не обрабатываются, можно переместить их в `_pages`:

1. Создайте папку `_pages`
2. Переместите все markdown файлы туда, сохранив структуру папок
3. Обновите permalinks соответственно

Но сначала попробуйте текущее решение - оно должно работать.

## Проверка структуры файла:

Убедитесь, что файл `00_introduction/01_goals_and_objectives.md` имеет такую структуру:

```yaml
---
layout: default
title: Цель и задачи книги
permalink: /00_introduction/01_goals_and_objectives.html
---

# Цель и задачи книги
...
```

## Важные замечания:

- **baseurl** в `_config.yml` должен быть `/petro_ml_book` (с ведущим слэшем)
- **permalinks** в файлах НЕ должны содержать baseurl (Jekyll добавляет его автоматически)
- Все ссылки должны использовать фильтр `relative_url` для правильной работы с baseurl

## Если ничего не помогает:

1. Проверьте, что репозиторий **публичный** (для бесплатного GitHub Pages)
2. Убедитесь, что в репозитории есть файл `.github/workflows/pages.yml`
3. Попробуйте очистить кеш в Settings → Pages → "Clear cache"
4. Создайте новый коммит с небольшим изменением, чтобы запустить пересборку

---

**После пуша изменений подождите 2-3 минуты и проверьте URL снова.**

