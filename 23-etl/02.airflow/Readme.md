# Airflow

# План рассказа ETL Airflow - оркестрация ML процессов
Часть вторая - оркестрация через Airflow

Структура аналогична рассказу про Luigi:

1) Рассказ про инструмент Airflow, его принципы работы: DAG, задачи, зависимости
2) Показать аналогичный TF-IDF пайплайн на Airflow
3) Подвести итоги и сравнение с Luigi

# ДЗ

Выбрать любой из рассказанных оркестраторов и перевести пайплайн под другой датасет в использованием рассказанных фич.

# Воспроизводимость пайплайна

Для воспроизводимости пайплайна необходимо скачать датасет в папку "Amazon Reviews" и в окружении вызвать:
```{python}
python setup.py
```

Проверяем, что появились файлы в папке 2.etl_airflow/dags/data. Поскольку airflow работает по расписанию, нужно убедиться, что у файлов есть в названии есть дата в формате YYMMDD (пример: train_20240120.csv).

Для корретной работы airflow необходимо создать папки dags, logs, plugins.
Перед запуском airflow требуется задать airflow_uid, чтобы избежать сложностей с права на запись логов. 
```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```
Для запуска airflow используем команду. 
```bash
docker compose up
```
Airflow доступен по localhost:8080. Логин и пароль - airflow. 
Запуск airflow занимает некоторое время, поскольку состоит из нескольких контейнеров.
После запуска нужно запустить DAG в web интерфейсе. 

### Как запустить airflow локально и с использование Docker Compose?

Сначала попробуем скачать airflow, потом запустим его уже в Docker. Ниже инструкция.
1. Создаем виртуальное окружение (любое абсолютно) и активируем его. Зачем? Airflow установит много нужных ему библиотек, так не повлияет на работу над другими проектами.
2. Задаем переменную окружения airflow_home. Именно туда установится airflow, можно задать удобный путь
```Shell
export AIRFLOW_HOME= {your path}
```
3. Проверим, что выбранная нами версия airflow совместима с установленной версией Python. 
4. Можно использовать текущий скрипт, чтобы установить airflow. Почему ставим через pip? Это рекомендуемый способ от разработчиков, через poetry не рекомендуют. 
```Bash
AIRFLOW_VERSION=2.7.1
# Extract the version of Python you have installed.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.7.1 with python 3.8: https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

5. Инициализируем БД (она нужна airflow для хранения состояния задач и прочих метаданных)
```Shell
airflow db init
```
6. Запускаем веб-сервер, можно через -p задать желаемый порт (по умолчанию 8080)
```shell
airflow webserver 
```
7. Заведем нового пользователя
```Shell
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@admin.org
```
Теперь можем получить доступ к веб-интерфейсу - localhost:8080
8. Запустим планировщик
```Shell
airflow scheduler
```
9. Полезная команда c различными командами для airflow
```Shell
airflow cheat-sheet
```

В файле airflow.cfg можно изменить настройки airflow. Например, заменить базу данных с SQLite на другую, поменять Executor. 

Теперь перейдем к запуску airflow в докере, что позволит нам как задать другую БД и executor.
Сначала необходимо убедиться, что на docker выделена память от 4 ГБ, а лучше 8 ГБ. 
Скачаем docker-compose файл и изучим его.
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
```
Docker compose файл содержит следующие сервисы:
- `airflow-scheduler` - планировщик, который мониторит все задачи и даги.
- `airflow-webserver` - веб-сервер, доступны на `http://localhost:8080`.
- `airflow-worker` - воркер, который выполняет команды планировщика.
- `airflow-triggerer` - The triggerer runs an event loop for deferrable tasks.
- `airflow-init` - инициализирует сервисы
- `postgres` - база данных
- `redis` - брокер сообщений для общения  планировщика и воркера.

Можно дополнительно включить flower, например `docker compose up flower`. Он обеспечит мониторинг, доступ на `http://localhost:5555`.

Все эти сервисы позволят запустить Airflow c CeleryExecutor. 

Необходимо еще настроить volumes. 
- `./dags` - здесь должны быть расположены даги
- `./logs` - здесь будут логи
- `./plugins` - здесь можно оставить кастомные плагины.

При этом будут загружены тестовые даги, которые можно будет попробовать запустить. 
Как запустить? 
Снимаем с паузы даг в веб-интерфейсе.
