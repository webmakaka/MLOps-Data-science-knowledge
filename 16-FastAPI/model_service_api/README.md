# Model Service Api

Example The ML service is a web application that provides an API for interacting with a machine learning model. It allows users to send queries with prediction data and get results back.

**Startup logic:**

When launched, the application initializes FastAPI, which handles HTTP requests. The app also connects to the machine learning model and loads it into memory for use in making predictions.

```
.
├── .docker
│   └── Dockerfile              # Файл Dockerfile для создания образа контейнера
├── pyproject.toml              # Файл с зависимостями и настройками проекта
├── .env                        # Файл с переменными окружения
├── docker-compose.yml          # Файл для управления контейнерами Docker
└── src
    ├── app.py                  # Основной файл приложения, инициализация FastAPI
    ├── api                     # Пакет с API роутами
    │   ├── __init__.py         # Инициализация пакета
    │   ├── routes              # Пакет с маршрутами API
    │   │   ├── __init__.py     # Инициализация пакета маршрутов
    │   │   ├── healthcheck.py  # Роут для проверки состояния сервиса
    │   │   ├── predict.py      # Роут для предсказаний модели
    │   │   └── router.py       # Основной маршрутизатор
    ├── schemas                  # Пакет с моделями данных
    │   ├── __init__.py         # Инициализация пакета
    │   ├── healthcheck.py      # Модель для ответов состояния сервиса
    │   └── requests.py         # Модель для входных запросов к API
    └── services                # Пакет с бизнес-логикой
        ├── __init__.py         # Инициализация пакета
        ├── model.py            # Логика работы с моделью машинного обучения
        └── utils.py            # Вспомогательные утилиты
```

## Getting started

```
docker-compose up --build
```
web-server on
```
http://0.0.0.0:7007
```
swagger ui on
```
http://0.0.0.0:7007/docs
```
For test
```
curl -X 'POST' \
  'http://0.0.0.0:7007/api/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Привет, как дела? Что нового?"
}'
```