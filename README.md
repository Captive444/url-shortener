# URL Shortener Service

Сервис для сокращения ссылок (аналог bitly). Написан на FastAPI с использованием SQLite.  
Есть веб-интерфейс и API документация.

---

##  Функциональность

-  Создание короткой ссылки из длинной (`POST /shorten`)
-  Редирект по короткой ссылке на оригинал (`GET /{short_id}`)
-  Автоматический счётчик переходов (увеличивается при каждом переходе)
-  Статистика переходов (`GET /stats/{short_id}`)
-  Простой веб-интерфейс для удобства (`/ui`)
-  Автоматическая документация API (`/docs`)
-  Unit-тесты (pytest)

---

##  Технологии

- Python 3.11
- FastAPI - веб-фреймворк
- SQLite + SQLAlchemy (async) — база данных и ORM
- Pydantic - валидация данных
- Uvicorn - ASGI сервер
- Docker + docker-compose — контейнеризация
- Pytest - тестирование

---
##  Запуск проекта

### Способ 1. Через Docker (проще всего)

Если у вас установлен Docker:

```bash
# 1. Скачиваем проект
git clone https://github.com/Captive444/url-shortener.git
cd url-shortener

# 2. Запускаем
docker-compose up -d

# 3. Открываем в браузере
http://localhost:8000/ui
