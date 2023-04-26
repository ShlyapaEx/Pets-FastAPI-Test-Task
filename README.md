# Consyst-OS FastAPI Test Task

Результат выполнения тестового задания на должность Junior Python Developer в компанию Консист-ОС.

Суть задания — создание маленького сервиса, позволяющего читать, создавать и удалять питомцев из базы данных. В качестве дополнительного задания я решил добавить возможность редактирования питомцев.

С полным текстом задания можно ознакомиться здесь: [https://disk.yandex.ru/i/oj74KNGB5ixpXQ](https://disk.yandex.ru/i/oj74KNGB5ixpXQ).

---

## Используемые библиотеки

- [FastAPI](https://github.com/tiangolo/fastapi) v.0.95.1
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) v.2.0.10
- [Alembic](https://github.com/sqlalchemy/alembic) v.1.10.3
- [asyncpg](https://github.com/MagicStack/asyncpg) v.0.27.0

---

## **Структура проекта**

Весь код проекта находится внутри директории `/app`. Вне этой директории находятся служебные файлы. Файл с конфигурацией самого приложения — `/app/config.py`.

---

## Настройка приложения перед запуском

Настройки приложения берутся из переменных окружения.

Перед запуском необходимо переименовать файл `.env.template` в корне проекта в `.env` и, при необходимости, отредактировать его.

---

## Запуск приложения через Docker

1. После завершения настройки для запуска приложения через Docker достаточно прописать в терминал одну команду:

   ```bash
   docker-compose up -d
   ```

2. Для остановки приложения нужно выполнить команду:

   ```bash
   docker-compose down
   ```

---

## Работа с приложением

Работа с приложением ведётся путём отправки ему HTTP-запросов. Для ознакомления со списком доступных маршрутов и для их тестирования можно перейти по адресу: [http://localhost:3000/docs](http://localhost:3000/docs) (после запуска приложения на своём компьютере через Docker)

---

## Внешний вид страницы с документацией приложения

![/docs swagger image](https://user-images.githubusercontent.com/98982398/234563432-116c5feb-6a6f-43aa-af50-44610aee2fcc.png)
