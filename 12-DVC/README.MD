# DVC example
## Установка окружения

Установка виртуального окружения conda
```bash
conda create -f env.yaml
conda activate mlops-dvc
```

Установка зависимостей окружения poetry
```bash
poetry install
```

## Скачивание данных
Скачиваем только сырые данные
```bash
dvc pull data/train.csv.dvc
```
## Запуск пайплайна
запустить все шаги исследования
```sh
dvc repro
```