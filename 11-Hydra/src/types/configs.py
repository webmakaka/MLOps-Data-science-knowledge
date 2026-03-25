from dataclasses import dataclass, field
from omegaconf import MISSING
from typing import Any


@dataclass
class PreprocessingConfig:
    padding: str = "max_length"
    max_length: int = 512
    tokenizer_name: str = MISSING
    test_size: int = 10000
    train_size: int = 50000


@dataclass
class RobertaPreprocessing(PreprocessingConfig):
    max_length: int = 256
    tokenizer_name: str = "siebert/sentiment-roberta-large-english"
    test_size: int = 5000
    train_size: int = 20000


@dataclass
class DistillBertPreprocessing(PreprocessingConfig):
    tokenizer_name: str = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"


@dataclass(frozen=True)
class ModelConfig:
    _target_: str = "transformers.AutoModelForSequenceClassification.from_pretrained"
    _convert_: str = "object"
    pretrained_model_name_or_path: str = MISSING
    problem_type: str = "single_label_classification"


@dataclass(frozen=True)
class RobertaModel(ModelConfig):
    pretrained_model_name_or_path: str = "siebert/sentiment-roberta-large-english"


@dataclass(frozen=True)
class DistillBertModel(ModelConfig):
    pretrained_model_name_or_path: str = (
        "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    )
    num_labels: int = 2
    ignore_mismatched_sizes: bool = True


@dataclass
class TrainingConfig:
    _target_: str = "transformers.TrainingArguments"
    output_dir: str = MISSING
    evaluation_strategy: str = "epoch"
    save_strategy: str = "epoch"
    learning_rate: float = 2e-5
    per_device_train_batch_size: int = 64
    per_device_eval_batch_size: int = 64
    num_train_epochs: int = 3
    weight_decay: float = 0.01
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "f1"
    fp16: bool = True


@dataclass
class DistillBertTraining(TrainingConfig):
    output_dir: str = "distillbert_training_outputs"


@dataclass
class RobertaTraining(TrainingConfig):
    output_dir: str = "roberta_training_outputs"
    per_device_train_batch_size: int = 24
    per_device_eval_batch_size: int = 24


defaults = [
    {"preprocessing": "distillbert"},
    {"model": "distillbert"},
    {"training": "distillbert"},
]


@dataclass
class MainConfig:
    defaults: list[Any] = field(default_factory=lambda: defaults)
    preprocessing: PreprocessingConfig = MISSING
    model: ModelConfig = MISSING
    training: TrainingConfig = MISSING

    
    
