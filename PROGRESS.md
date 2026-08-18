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
- [x] Модель Offer + миграция (предложения курьеров)
- [x] Эндпоинты предложений: POST /items/{id}/offers, GET /items/{id}/offers
- [x] Модель Request + миграция (заявки получателей)
- [x] Эндпоинты заявок: POST /items/{id}/requests, GET /items/{id}/requests

## В работе
- (пусто)

## Следующие шаги
- [ ] Логика торгов (accept/reject для offer и request, статусы заказа)
- [ ] Скрытая доставка (приватная ссылка + токен)
- [ ] Уведомления
- [ ] Увеличить SECRET_KEY до 32+ байт (убрать InsecureKeyLengthWarning)

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
- База Neon на бесплатном плане "засыпает" при неактивности — нужно разбудить через console.neon.tech или подождать 30-60 секунд
- Добавили sslmode=require и connect_timeout=30 в database.py для стабильности
- migrations/env.py использует NullPool и connectable.begin() для корректной работы с asyncpg
- При работе через VPN база иногда "теряется" — это нормально, не критично для разработки