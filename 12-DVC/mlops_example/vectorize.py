import pickle
from pathlib import Path

import click
import dvc.api
import numpy as np
import polars as pl
import scipy as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from .cli import cli


def train_vectorize(
    data: pl.DataFrame,
) -> tuple[TfidfVectorizer, pl.DataFrame, pl.DataFrame]:
    params = dvc.api.params_show()

    tfidf_vectorizer = TfidfVectorizer(**params["vectorizer_tfidf"])

    train, val = train_test_split(
        data,
        test_size=params["test_train_split"],
        shuffle=True,
        random_state=params["random_state"],
    )
    tfidf_vectorizer.fit(train["corpus"].list.join(" ").to_numpy())
    return tfidf_vectorizer, train, val


def apply_vectorizer(vectorizer: TfidfVectorizer, data: pl.DataFrame) -> pl.DataFrame:
    return vectorizer.transform(data["corpus"].list.join(" ").to_numpy())


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("vectorizer_path", type=Path)
@click.argument("train_features_path", type=Path)
@click.argument("val_features_path", type=Path)
def cli_train_vectorizer(
    input_frame_path: Path,
    vectorizer_path: Path,
    train_features_path: Path,
    val_features_path: Path,
):
    data = pl.read_parquet(input_frame_path)
    vectorizer, train, val = train_vectorize(data)
    pickle.dump(vectorizer, vectorizer_path.open("wb"))
    train.write_parquet(train_features_path)
    val.write_parquet(val_features_path)


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("vectorizer_path", type=Path)
@click.argument("result_frame_path", type=Path)
@click.argument("target_frame_path", type=Path)
def cli_apply_vectorizer(
    input_frame_path: Path,
    vectorizer_path: Path,
    result_frame_path: Path,
    target_frame_path: Path,
):
    data = pl.read_parquet(input_frame_path)
    vectorizer = pickle.load(vectorizer_path.open("rb"))
    result = apply_vectorizer(vectorizer, data)
    sp.sparse.save_npz(result_frame_path, result)
    np.save(target_frame_path, data["Polarity"].to_numpy())
