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
- [x] Логика торгов: accept/reject для offers (POST /items/{id}/offers/{offer_id}/accept|reject)
- [x] Логика торгов: accept/reject для requests (POST /items/{id}/requests/{request_id}/accept|reject)
- [x] Статусы для Offer (pending/accepted/rejected)
- [x] Скрытая доставка: is_private + private_token для Items
- [x] Эндпоинт для скрытых доставок: GET /items/private/{token}
- [x] Увеличен SECRET_KEY до 32+ байт (secrets.token_urlsafe(32))

## В работе
- (пусто)

## Следующие шаги
- [ ] Уведомления (email/push при изменении статусов)
- [ ] Статус completed/cancelled для Items
- [ ] История заказов пользователя

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
- При работе через VPN база иногда "теряется" — это нормально, не критично для разработки
- Миграция a1b2c3d4e5f6 добавляет status в offers и is_private/private_token в items