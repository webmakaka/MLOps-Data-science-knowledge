import polars as pl
from preprocessing import LemmatizeWords
from luigi import DictParameter, LocalTarget, Task
from sklearn.model_selection import train_test_split


class PrepareTrainTestSplit(Task):
    """Split input files into train and test groups."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(PrepareTrainTestSplit, self).__init__(*args, **kwargs)
        self.output_path = self.task_dict_config["train_path"]  # только один output

    def requires(self) -> Task:
        return LemmatizeWords(self.task_dict_config)

    def run(self) -> None:
        input_frame = pl.read_parquet(self.requires().output().path)

        train, test = train_test_split(
            input_frame,
            test_size=0.3,
            shuffle=True,
            random_state=self.task_dict_config["random_state"],
        )

        train.write_parquet(self.task_dict_config["train_path"])
        test.write_parquet(self.task_dict_config["test_path"])

    def output(self) -> LocalTarget:
        return LocalTarget(self.output_path)
