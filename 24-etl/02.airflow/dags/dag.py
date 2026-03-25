from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from preprocessing import download_stopwords, clean_text_task, lemmatize_words
from config import task_config
from train_test_split import prepare_train_test_split
from tf_idf_features import train_tfidf_vectorizer
from logistic_model import train_tfidf_logistic_regression_model
from evaluation_model import evaluate_tfidf_model

start_date = datetime.today() - timedelta(days=2)

with DAG(
    dag_id="etl_airflow",
    description="Airflow pipeline",
    start_date=start_date,
    catchup=True,
    tags=["example"],
    schedule="@daily"
) as dag:
    download_stopwords = PythonOperator(
        task_id="download_stopwords",
        python_callable=download_stopwords,
    )

    clean_text = PythonOperator(
        task_id="clean_text",
        python_callable=clean_text_task,
        op_kwargs={
            "raw_file": f'{task_config["raw_file"]}_{{{{ ds_nodash }}}}.csv',
            "output_path": f'{task_config["clean_text_file"]}_{{{{ ds_nodash }}}}.parquet',
        },
        depends_on_past=True
    )

    lemmatize_words = PythonOperator(
        task_id="lemmatize_words",
        python_callable=lemmatize_words,
        op_kwargs={
            "input_path": f'{task_config["clean_text_file"]}_{{{{ ds_nodash }}}}.parquet',
            "output_path": f'{task_config["lemmatized_file"]}_{{{{ ds_nodash }}}}.parquet',
        },
        depends_on_past=True
    )

    prepare_train_test_split = PythonOperator(
        task_id="prepare_train_test_split",
        python_callable=prepare_train_test_split,
        op_kwargs={
            "input_path": f'{task_config["lemmatized_file"]}_{{{{ ds_nodash }}}}.parquet',
            "output_path": f'{task_config["train_path"]}__{{{{ ds_nodash }}}}.parquet',
            "random_state": task_config["random_state"],
            "train_path": f'{task_config["train_path"]}_{{{{ ds_nodash }}}}.parquet',
            "test_path": f'{task_config["test_path"]}_{{{{ ds_nodash }}}}.parquet',
        },
        depends_on_past=True
    )

    train_tfidf_vectorizer = PythonOperator(
        task_id="train_tfidf_vectorizer",
        python_callable=train_tfidf_vectorizer,
        op_kwargs={
            "input_path": f'{task_config["train_path"]}_{{{{ ds_nodash }}}}.parquet',
            "output_path": f'{task_config["vectorizer_path"]}_{{{{ ds_nodash }}}}.vect',
            "analyzer": task_config["analyzer"],
            "max_features": task_config["max_features"],
        },
        depends_on_past=True
    )

    train_tfidf_logistic_regression_model = PythonOperator(
        task_id="train_tfidf_logistic_regression_model",
        python_callable=train_tfidf_logistic_regression_model,
        op_kwargs={
            "output_path": f'{task_config["lr_model_path"]}_{{{{ ds_nodash }}}}.pkl',
            "input_vectorizer": f'{task_config["vectorizer_path"]}_{{{{ ds_nodash }}}}.vect',
            "train_frame": f'{task_config["train_path"]}_{{{{ ds_nodash }}}}.parquet',
            "random_state": task_config["random_state"],
            "multi_class": task_config["multi_class"],
            "solver": task_config["solver"],
        },
        depends_on_past=True
    )

    evaluate_tfidf_model = PythonOperator(
        task_id="evaluate_tfidf_model",
        python_callable=evaluate_tfidf_model,
        op_kwargs={
            "input_model": f'{task_config["lr_model_path"]}_{{{{ ds_nodash }}}}.pkl',
            "input_vectorizer": f'{task_config["vectorizer_path"]}_{{{{ ds_nodash }}}}.vect',
            "test_path": f'{task_config["test_path"]}_{{{{ ds_nodash }}}}.parquet',
            "report_file_path": f'{task_config["report_file_path"]}_{{{{ ds_nodash }}}}.json',
            "conf_matrix_path": f'{task_config["conf_matrix_path"]}_{{{{ ds_nodash }}}}.png',
        },
        depends_on_past=True
    )

    download_stopwords >> clean_text >> lemmatize_words >> prepare_train_test_split
    prepare_train_test_split >> train_tfidf_vectorizer >> train_tfidf_logistic_regression_model 
    train_tfidf_logistic_regression_model >> evaluate_tfidf_model
