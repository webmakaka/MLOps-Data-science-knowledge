import json
import pickle
from pathlib import Path

import click
import dvc
import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
)

from .cli import cli


def conf_matrix(y_true: np.ndarray, pred: np.ndarray) -> Figure:
    plt.ioff()
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, pred, ax=ax, colorbar=False)
    ax.xaxis.set_tick_params(rotation=90)
    _ = ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


def train(data: np.ndarray, target: np.ndarray) -> LogisticRegression:
    model_params = dvc.api.params_show()
    model_lr = LogisticRegression(**model_params["logitic_regression"])
    model_lr.fit(data, target)
    return model_lr


def test(
    model: LogisticRegression, data: np.ndarray, target: np.ndarray
) -> tuple[dict, Figure]:
    predicts = model.predict(data)
    fig = conf_matrix(target, predicts)
    return classification_report(target, predicts, output_dict=True), fig


@cli.command()
@click.argument("train_frame_path", type=Path)
@click.argument("train_target_path", type=Path)
@click.argument("model_path", type=Path)
def cli_train(
    train_frame_path: Path,
    train_target_path: Path,
    model_path: Path,
):
    train_features = sp.sparse.load_npz(train_frame_path)
    train_target = np.load(train_target_path)
    model = train(train_features, train_target)
    pickle.dump(model, model_path.open("wb"))


@cli.command()
@click.argument("test_frame_path", type=Path)
@click.argument("test_target_path", type=Path)
@click.argument("model_path", type=Path)
@click.argument("metric_path", type=Path)
@click.argument("figure_path", type=Path)
def cli_test(
    test_frame_path: Path,
    test_target_path: Path,
    model_path: Path,
    metric_path: Path,
    figure_path: Path,
):
    test_features = sp.sparse.load_npz(test_frame_path)
    test_target = np.load(test_target_path)
    model = pickle.load(model_path.open("rb"))
    result, fig = test(model, test_features, test_target)
    json.dump(result, metric_path.open("w"))
    plt.savefig(figure_path)
