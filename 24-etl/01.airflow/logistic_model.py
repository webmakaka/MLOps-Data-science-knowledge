import pickle

import polars as pl
from tf_idf_features import TrainTfidfVectorizer
from train_test_split import PrepareTrainTestSplit
from luigi import DictParameter, LocalTarget, Task
from sklearn.linear_model import LogisticRegression


class TrainTfidfLogisticRegressionModel(Task):
    """Train log reg on tfidf features."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(TrainTfidfLogisticRegressionModel, self).__init__(*args, **kwargs)
        self.output_model = self.task_dict_config["lr_model_path"]

    def requires(self) -> list[Task]:
        return [
            TrainTfidfVectorizer(self.task_dict_config),
            PrepareTrainTestSplit(self.task_dict_config),
        ]

    def run(self) -> None:
        with open(self.requires()[0].output().path, "rb") as input_vectorizer:
            vectorizer = pickle.load(input_vectorizer)

        train_frame = pl.read_parquet(self.requires()[1].output().path)
        train_features = vectorizer.transform(
            train_frame["corpus"].to_pandas().astype(str)
        )

        model_log_reg = LogisticRegression(
            random_state=self.task_dict_config["random_state"],
            multi_class=self.task_dict_config["multi_class"],
            solver=self.task_dict_config["solver"],
        )

        model_log_reg.fit(train_features, train_frame["Polarity"])
        with open(self.output_model, "wb") as output_model_file:
            pickle.dump(model_log_reg, output_model_file)

    def output(self) -> LocalTarget:
        return LocalTarget(self.output_model)
