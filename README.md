# InterviewIQ

`InterviewIQ` - мобильное приложение для подготовки к HR-собеседованиям. Пользователь выбирает роль, уровень опыта, тему вопроса, сложность, лимит времени и количество вопросов, проходит практическую сессию, получает оценку ответа и видит прогресс в аналитике.

Вопросы для приложения взяты из датасета [HR Interview Questions and Ideal Answers](https://www.kaggle.com/datasets/aryan208/hr-interview-questions-and-ideal-answers)

## Функционал приложения

- Регистрация, вход и сохранение пользовательской сессии.
- Выбор профессии и уровня опыта.
- Подбор вопросов по профессии пользователя, теме и сложности.
- Практическая сессия на 5, 10, 15 или 20 вопросов.
- Текстовый и голосовой ответ.
- Загрузка аудио в MinIO/S3 с локальным fallback в `backend/.audio_uploads`.
- Транскрибация голосовых ответов через Faster Whisper.
- Анализ ответа через GigaChat или baseline эвристики.
- Защита от пустых и мусорных ответов: такие ответы получают `0`.
- Результаты по ответу: score, сильные стороны, варианты улучшения, ошибки.
- Firebase Cloud Messaging для push-уведомлений.

## Технологический Стек

- Frontend: `NativeScript`, `Vue 3`, `TypeScript`, `XState`;
- Backend: `FastAPI`, `SQLAlchemy`, `Alembic`, `PostgreSQL`;
- ML/LLM: `GigaChat`, `Faster Whisper`, baseline эвристики;
- Storage: `MinIO/S3`, локальный fallback для аудио;
- Push: `Firebase Cloud Messaging`.

## Структура проекта

```text
app/                  Мобильное приложение NativeScript
backend/app/          FastAPI backend
backend/alembic/      Миграции БД
backend/postman/      Postman collection
dataset/              Локальный датасет, не закоммичен
ml/                   Анализ и транскрибация ответов
```

## Технические требования

- Node.js 20+
- NativeScript CLI
- Python 3.11+
- PostgreSQL
- Android Emulator или реальный Android-телефон; IOS эмулятор или IOS устройство.
- MinIO, если нужен S3 загрузка без локального хранения аудио.

## Переменные окружения backend

Создайте файл `backend/api.env`, содержащий основные настройки хранилища, БД, а также ключи доступа. **Обязательно** поместите его в .gitignore, что не допустить утечки secret_key в открытый доступ!

Пример файла `api.env`:

```env
APP_NAME=InterviewIQ API
APP_VERSION=0.1.0
API_PREFIX=/api/v1

DATABASE_URL=postgresql+psycopg://interviewiq:password@localhost:5432/interviewiq

S3_ENDPOINT_URL=http://127.0.0.1:9000
S3_PUBLIC_URL=http://127.0.0.1:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=interviewiq-audio
S3_REGION=us-east-1

ANALYZER_PROVIDER=baseline
GIGACHAT_CREDENTIALS=
GIGACHAT_MODEL=GigaChat
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_VERIFY_SSL_CERTS=false
ANALYZER_TIMEOUT_SEC=20
MAX_ANSWER_CHARS=6000

WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8

FCM_PROJECT_ID=
FCM_SERVICE_ACCOUNT_PATH=
FCM_SERVER_KEY=
```

Для демонстрации можно оставить `ANALYZER_PROVIDER=baseline`, тогда оценка ответа будет происходить с помощью эвристик. Если MinIO недоступен, приложение сохранит аудио локально в `backend/.audio_uploads`.

## Запуск backend

```bash
cd backend
python -m venv .venv
source .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Загрузка вопросов

Сначала можно загрузить небольшой встроенный набор:

```bash
cd backend
source .venv\Scripts\activate
python -m app.scripts.seed_questions
```

Для загрузки основого датасета сначала его необходимо [скачать](https://www.kaggle.com/datasets/aryan208/hr-interview-questions-and-ideal-answers) и поместить в корневую папку `dataset/`. После этого запустите команду, которая позволит вам загрузить датасет в PostgreSQL:

```bash
python -m app.scripts.seed_dataset_questions --path ../dataset/hr_interview_questions_dataset.json
```

Чтобы загрузить часть датасета в БД, используйте флаг `--limit [value]`:

```bash
python -m app.scripts.seed_dataset_questions --path ../dataset/hr_interview_questions_dataset.json --limit 1000
```

## Запуск frontend

Из корня проекта:

```bash
npm install
ns run android
```

Android Emulator обращается к backend через:

```text
http://10.0.2.2:8000/api/v1
```

Локальный iOS/desktop runtime использует:

```text
http://127.0.0.1:8000/api/v1
```

## Основной пользовательский flow

1. Пользователь регистрируется или входит.
2. Проходит onboarding: выбирает профессию и уровень опыта.
3. На PracticePage выбирает тему, сложность, время и количество вопросов.
4. Отвечает текстом или голосом.
5. Получает анализ ответа на ResultsPage.
6. Переходит к следующему вопросу или завершает сессию.
7. После завершения видит обновленные Home, Analytics и Profile.

## Важные ограничения MVP

- Приложение сейчас сфокусировано на HR-вопросах, потому что основной датасет содержит только HR вопросы с интервью.
- Dark Mode пока является настройкой-заготовкой, полноценная темизация требует отдельного прохода по стилям.
