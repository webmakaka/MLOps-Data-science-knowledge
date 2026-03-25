import json
import pickle

import numpy as np
import polars as pl
from logistic_model import TrainTfidfLogisticRegressionModel
from tf_idf_features import TrainTfidfVectorizer
from train_test_split import PrepareTrainTestSplit
from luigi import DictParameter, LocalTarget, Task
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn.metrics import ConfusionMatrixDisplay, classification_report


def conf_matrix(y_true: np.ndarray, pred: np.ndarray) -> Figure:
    plt.ioff()
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, pred, ax=ax, colorbar=False)
    ax.xaxis.set_tick_params(rotation=90)
    _ = ax.set_title(f"Confusion Matrix")
    plt.tight_layout()
    return fig


class EvaluateTfidfModel(Task):
    """Get top words with importance from log reg coefs and tfidf features."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(EvaluateTfidfModel, self).__init__(*args, **kwargs)
        self.conf_matrix_path = self.task_dict_config["conf_matrix_path"]

    def requires(self) -> list[Task]:
        return [
            TrainTfidfLogisticRegressionModel(self.task_dict_config),
            TrainTfidfVectorizer(self.task_dict_config),
            PrepareTrainTestSplit(self.task_dict_config),
        ]

    def run(self) -> None:
        with open(self.requires()[0].output().path, "rb") as input_model:
            model_log_reg = pickle.load(input_model)

        with open(self.requires()[1].output().path, "rb") as input_vectorizer:
            vectorizer = pickle.load(input_vectorizer)

        test_frame = pl.read_parquet(self.task_dict_config["test_path"])
        test_features = vectorizer.transform(
            test_frame["corpus"].to_pandas().astype(str)
        )

        predicts = model_log_reg.predict(test_features)
        report = classification_report(
            test_frame["Polarity"], predicts, output_dict=True
        )
        with open(self.task_dict_config["report_file_path"], "w") as report_file:
            json.dump(report, report_file, indent=4)

        confusion_matrix_fig = conf_matrix(test_frame["Polarity"], predicts)

        confusion_matrix_fig.figure.savefig(
            self.conf_matrix_path,
            transparent=False,
            facecolor="white",
            bbox_inches="tight",
        )
        plt.close(confusion_matrix_fig)

    def output(self) -> LocalTarget:
        return LocalTarget(self.conf_matrix_path)
