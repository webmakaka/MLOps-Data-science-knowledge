# Luigi

Для воспроизведения окружения необходимо установить anaconda или micromamba:

## Create virtual environment

Create and activate `micromamba` virtual environment:

```bash
micromamba env create -f env.yaml
micromamba activate mlops-luigi
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

Окружение такое же, что и в mlflow.

# План рассказа ETL - оркестрация ML процессов
Часть первая - оркестрация через Luigi

1) Пройтись по слайдам, рассказать, что доступно в Luigi
2) Демо: показать пример оформленного пайплайна NLP для TF-IDF
3) Подвести итоги использования luigi

# Воспроизводимость пайплайна

Для воспроизводимости пайплайна необходимо скачать датасет в папку "Amazon Reviews" и в окружении вызвать:
```{python}
python setup.py
```

Чтобы запустить пайплайн, в окружении можно воспользоваться командой:
```{python}
python etl_pipelines.py
```