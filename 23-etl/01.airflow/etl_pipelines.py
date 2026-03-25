import os

import luigi
from evaluation_model import EvaluateTfidfModel
from logistic_model import TrainTfidfLogisticRegressionModel
from preprocessing import CleanText, LemmatizeWords
from tf_idf_features import TrainTfidfVectorizer
from train_test_split import PrepareTrainTestSplit


def tf_idf_pipeline() -> None:
    """tf-idf example pipeline."""

    for project_dir in ["raw", "interim", "prepared"]:
        os.makedirs(f"data/{project_dir}", exist_ok=True)

    task_config = {
        "raw_file": "data/raw/train_50k.csv",
        "clean_text_file": "data/interim/clean_text.parquet",
        "lemmatized_file": "data/interim/lemmatized_file.parquet",
        "train_path": "data/interim/train_samples.parquet",
        "test_path": "data/interim/test_samples.parquet",
        "vectorizer_path": "data/prepared/vectorizer.vect",
        "lr_model_path": "data/prepared/tf_idf_log_reg.pkl",
        "conf_matrix_path": "data/prepared/tf_idf_conf_matrix.png",
        "report_file_path": "data/prepared/tf_idf_report.json",
        "random_state": 42,
        "max_features": 10000,
        "analyzer": "word",
        "multi_class": "multinomial",
        "solver": "saga",
    }
    pipeline = [
        CleanText(task_config),
        LemmatizeWords(task_config),
        PrepareTrainTestSplit(task_config),
        TrainTfidfVectorizer(task_config),
        TrainTfidfLogisticRegressionModel(task_config),
        EvaluateTfidfModel(task_config),
    ]
    luigi.build(pipeline, local_scheduler=True)


if __name__ == "__main__":
    tf_idf_pipeline()
