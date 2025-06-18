# LearnCoreAPI - Бэкенд для платформы онлайн-обучения

## 📌 Описание проекта

LearnCoreAPI — это бэкенд-система для платформы онлайн-обучения (LMS), предоставляющая RESTful API для управления курсами и учебными материалами.

---
## Основные возможности
- Создание и управление курсами и уроками
- Система аутентификации и авторизации пользователей
- Загрузка учебных материалов (тексты, изображения, файлы)
- Отслеживание прогресса обучения
- RESTful API интерфейс
- Поддержка PostgreSQL
- Кэширование с Redis
- Конфигурация через переменные окружения

## 🛠 Технологии

- Python 3.9+
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL
- Redis
- Poetry (управление зависимостями)

---

## 🚀 Установка и запуск 
  
1. Клонировать репозиторий:  
   ```bash  
   git clone https://github.com/yourusername/LearnCoreAPI.git
   cd LearnCoreAPI

2. Установка Poetry и зависимостей.
  ```bash
  pip install poetry
  ```
Затем:  
  ```bash    
  poetry install.
  ```
3. Активация виртуального окружения
```bash
poetry shell  
```  
4. Применение миграций и создание администратора  
```bash  
python manage.py migrate  
python manage.py createsuperuser 

```
5. Запуск проекта  
```bash
python manage.py runserver  
```





