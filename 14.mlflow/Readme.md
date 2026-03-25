# Mlflow

Для воспроизведения окружения необходимо установить anaconda или micromamba:

## Create virtual environment

Create and activate `micromamba` virtual environment:

```bash
micromamba env create -f env.yaml
micromamba activate mlops-mlflow
```

### Poetry initial setup

Configure `poetry` (`~/micromamba/envs` is path to your envs folder):

```bash
poetry config virtualenvs.in-project false --local
poetry config virtualenvs.path ~/micromamba/envs --local
```

Install dependencies with `poetry`:

```bash
poetry install
```

# План рассказа MLFlow - трекинг экспериментов

1) Рассказать общие идеи MLFlow как инструмента

2) Показать на практике: пример задачи Sentiment Analysis на Amazon Reviews
Датасет: https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews

Перед тем как перезапускать ноутбуки необходимо скачать датасет в папку "Amazon Reviews"

2.1) tf_idf_amazon.ipynb
- Рассказать в целом про размеры датасета
- Анализ данных: препроцессинг, текстовый препроцессинг
- Получение фичей, обучение TF-IDF модели
- Метьрики, использование MLFlow, чтобы затрекать результат
2.2) bert_amazon.ipynb
- Повторение эксперимента, но с получением эмбеддингов от берта
- Обучение логистической регрессии поверх эмбеддингов
- Сравнение результатов в MLFlow, сравнение результатов

# Дз

Выделить 2-3 эксперимента на своем датасете, протестировать подходы и выбрать лучший на основе трекинга MLFlow.