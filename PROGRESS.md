# CargoPeer — прогресс разработки

## Готово
- [x] Настроена среда разработки (VS Code + Git + uv) на двух ПК
- [x] Настроен GitHub + Settings Sync (синхронизация IDE между ПК)
- [x] Подключена облачная PostgreSQL (Neon)
- [x] Настроен Alembic для миграций
- [x] Создана модель User и таблица в базе
- [x] Эндпоинт регистрации POST /auth/register (с хешированием паролей)
- [x] Эндпоинт входа POST /auth/login (с JWT-токенами на 24 часа)
- [x] Защищённый эндпоинт GET /auth/me (проверка токена)
- [x] Модель Item + миграция (товар на полке)
- [x] Эндпоинты полки: POST /items, GET /items, GET /items/{id}

## В работе — предложения курьеров (Offer)
**Что сделано:**
- [x] Обновлена модель models.py (добавлен класс Offer с связями)
- [x] Обновлена schemas.py (добавлены OfferCreate, OfferOut)
- [x] Создан routers/offers.py (POST и GET для предложений)
- [x] Обновлён main.py (подключён offers_router)
- [x] Обновлён migrations/env.py (использует NullPool)
- [x] Обновлён app/database.py (добавлены sslmode=require, connect_timeout=30)

**Что осталось сделать:**
- [ ] Разбудить базу Neon (зайти на console.neon.tech, нажать Resume)
- [ ] Создать миграцию: uv run python -m alembic revision --autogenerate -m "add offers table"
- [ ] Применить миграцию: uv run python -m alembic upgrade head
- [ ] Протестировать в Swagger:
  - Создать второго пользователя (курьера)
  - Получить токен курьера через /auth/login
  - Сделать POST /items/{item_id}/offers (предложение от курьера)
  - Проверить GET /items/{id}/offers (список предложений)
- [ ] Закоммитить: git add . ; git commit -m "feat: offers model and endpoints" ; git push

## Следующие шаги
- [ ] Модель Request (заявка получателя) + миграция
- [ ] Логика торгов (встречные предложения, статусы заказа)
- [ ] Скрытая доставка (приватная ссылка + токен)
- [ ] Уведомления

## Стек
- Python 3.12, FastAPI, SQLAlchemy (async), asyncpg, Alembic
- База: Neon PostgreSQL (облачная, бесплатная)
- JWT-токены через PyJWT
- uv для управления зависимостями

## Правила разработки
1. Коммитим после каждого шага, не в конце дня
2. Файлы создаём через PowerShell (.WriteAllText), не через VS Code UI
3. Начиная сессию — git status + git pull, смотрим реальное состояние
4. Секреты хранятся в .env (не коммитится), пароли в открытом виде нигде не храним

## Заметки
- База Neon на бесплатном плане "засыпает" при неактивности
- При первом запросе после простоя может быть ConnectionResetError — нужно подождать 30-60 секунд или разбудить через console.neon.tech
- Добавили sslmode=require и connect_timeout=30 в database.py для стабильности