import pickle

import polars as pl
from train_test_split import PrepareTrainTestSplit
from luigi import DictParameter, LocalTarget, Task
from sklearn.feature_extraction.text import TfidfVectorizer


class TrainTfidfVectorizer(Task):
    """Train vectorizers on train/test splits."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(TrainTfidfVectorizer, self).__init__(*args, **kwargs)
        self.output_vectorizer = self.task_dict_config["vectorizer_path"]

    def requires(self) -> Task:
        return PrepareTrainTestSplit(self.task_dict_config)

    def run(self) -> None:
        train_frame = pl.read_parquet(self.requires().output().path)
        tfidf_vectorizer = TfidfVectorizer(
            analyzer=self.task_dict_config["analyzer"],
            max_features=self.task_dict_config["max_features"],
        )

        tfidf_vectorizer.fit(train_frame["corpus"].to_pandas().astype(str))
        with open(self.output_vectorizer, "wb") as output:
            pickle.dump(tfidf_vectorizer, output)

    def output(self) -> LocalTarget:
        return LocalTarget(self.output_vectorizer)
