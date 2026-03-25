import polars as pl
from functools import partial
from sklearn.model_selection import train_test_split
from datasets import Dataset
from sklearn.metrics import (
    f1_score,
    accuracy_score,
)
from transformers import (
    AutoTokenizer,
    Trainer,
    EvalPrediction,
    EarlyStoppingCallback,
)
from typing import Any
import hydra
from hydra.utils import instantiate
from hydra.core.config_store import ConfigStore
import numpy as np
from omegaconf import DictConfig, OmegaConf
import logging
from src import (
    RobertaModel,
    RobertaPreprocessing,
    RobertaTraining,
    DistillBertModel,
    DistillBertPreprocessing,
    DistillBertTraining,
    MainConfig,
)


log = logging.getLogger(__name__)


def preprocess_frame(frame: pl.DataFrame):
    res = frame.with_columns(
        [
            ((pl.col("title") + " " + pl.col("text")).alias("text")),
            (pl.col("polarity").replace({1: 0, 2: 1})),
        ]
    )
    return res


def preprocess_sample(
    sample: dict[str, Any], tokenizer: AutoTokenizer, padding: str, max_length: int
) -> dict[str, Any]:
    """Encode input raw string to sequence of tokens.
    Also add corresponding labels.

    Args:
        sample (dict[str, Any]): dataset sample w/ <text-label> pair
        tokenizer (AutoTokenizer): model tokenizer

    Returns:
        dict[str, Any]: transformed sample with tokenized text and labels.
    """
    text = sample["text"]
    # каждый сэмпл паддится до самой длинной посл-ти в этом батче (padding="max_length")
    # макс. длина посл-ти 512 (max_length=512), все, что длиннее, обрезается (truncation=True)
    encoding = tokenizer(
        text,
        padding=padding,
        truncation=True,
        max_length=max_length,
    )
    encoding["labels"] = sample["labels"]
    return encoding


def compute_metrics(p: EvalPrediction) -> dict[str, float]:
    """Calculate metrics used on validation step.

    Args:
        p (EvalPrediction): container with predictions and
        ground-truth labels

    Returns:
        dict[str, float]: dictionary with computed labels
    """
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    preds = np.argmax(preds, axis=1)
    f1 = f1_score(p.label_ids, preds, average="macro")
    acc = accuracy_score(p.label_ids, preds)
    res = {"f1": f1, "accuracy": acc}
    return res


def make_dataset(
    frame: pl.DataFrame,
    tokenizer: AutoTokenizer,
    label2id: dict[str, int],
    prepr_conf: dict[str, Any],
    train_size: int = 0,
    test_size: int = 0,
) -> tuple[Dataset, Dataset]:
    """Create huggingface datasets used in training process.

    Args:
        frame (pl.DataFrame): input frame with text data
        tokenizer (AutoTokenizer): model tokenizer
        label2id (dict[str, int]): mapping from category text names
        to digital ids.
        test_size (float, optional): test split share. Defaults to None.

    Returns:
        tuple[Dataset, Dataset]: train & test splits, tokenized, vectorized and batched.
    """
    # переименуем столбцы для целостности с api hf-datasets
    clear_frame = frame.select(pl.col("text"), pl.col("polarity").alias("labels"))

    # перейдем от строковых названий к численным меткам
    clear_frame = clear_frame.with_columns(pl.col("labels").map_dict(label2id))

    # каррированная функция с фиксированным
    # токенизатором для дальнейшего исп-я в Dataset.map()
    part_prepr = partial(
        preprocess_sample,
        tokenizer=tokenizer,
        padding=prepr_conf["padding"],
        max_length=prepr_conf["max_length"],
    )

    train_df, test_df = train_test_split(
        clear_frame,
        test_size=test_size,
        train_size=train_size,
        random_state=42,
        stratify=clear_frame["labels"],
    )
    train_dataset = Dataset.from_pandas(train_df.to_pandas(), split="train")
    test_dataset = Dataset.from_pandas(test_df.to_pandas(), split="test")
    encoded_train = train_dataset.map(
        part_prepr, batched=True, remove_columns=train_dataset.column_names
    )
    encoded_test = test_dataset.map(
        part_prepr, batched=True, remove_columns=test_dataset.column_names
    )
    encoded_train.set_format("torch")
    encoded_test.set_format("torch")
    return encoded_train, encoded_test


def make_training_pipeline(
    tokenizer: AutoTokenizer,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    model_conf: dict[str, Any],
    train_conf: dict[str, Any],
    id2label: dict[int, str],
    label2id: dict[str, int],
) -> Trainer:
    """Training process wrapper.

    Args:
        exp_name (str): name of the local folder
        for saving model checkpoints.
        tokenizer (AutoTokenizer): model tokenizer
        train_dataset (Dataset): train dataset split
        eval_dataset (Dataset): test dataset split
        batch_size (int, optional): number of samples
        in sigle batch. Defaults to 32.
        lr (float, optional): model's learning rate. Defaults to 2e-5.
        epochs_num (int, optional):
        number of training iterations. Defaults to 20.

    Returns:
        Trainer: hf training pipeline abstraction class.
    """

    args = instantiate(train_conf)

    model = instantiate(
        model_conf, num_labels=len(id2label), id2label=id2label, label2id=label2id
    )

    trainer = Trainer(
        model,
        args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )
    return trainer


# cs = ConfigStore.instance()
# cs.store(group="preprocessing", name="distillbert", node=DistillBertPreprocessing)
# cs.store(group="preprocessing", name="roberta", node=RobertaPreprocessing)
# cs.store(group="model", name="distillbert", node=DistillBertModel)
# cs.store(group="model", name="roberta", node=RobertaModel)
# cs.store(group="training", name="distillbert", node=DistillBertTraining)
# cs.store(group="training", name="roberta", node=RobertaTraining)
# cs.store(name="config", node=MainConfig)


@hydra.main(version_base=None, config_path="src/conf", config_name="config")
def main(cfg: MainConfig):
    #log.info(cfg.preprocessing.pading)
    log.info(OmegaConf.to_yaml(cfg, resolve=True))
    # processed = preprocess_frame(frame)
    # tokenizer = AutoTokenizer.from_pretrained(cfg["preprocessing"]["tokenizer_name"])
    # label2id = processed["polarity"].unique().sort().to_list()
    # label2id = dict(zip(label2id, range(len(label2id))))
    # id2label = {v: k for k, v in label2id.items()}
    # train_ds, test_ds = make_dataset(
    #     processed,
    #     tokenizer,
    #     label2id,
    #     cfg["preprocessing"],
    #     cfg["preprocessing"]["test_size"],
    #     cfg["preprocessing"]["train_size"],
    # )
    # trainer = make_training_pipeline(
    #     tokenizer, train_ds, test_ds, cfg["model"], cfg["training"], id2label, label2id
    # )
    # trainer.train()


if __name__ == "__main__":
    frame = pl.read_csv(
        "data/train.csv", has_header=False, new_columns=["polarity", "title", "text"]
    )
    main()
