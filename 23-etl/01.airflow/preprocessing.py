import re

import polars as pl
from luigi import DictParameter, LocalTarget, Task
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def basic_clean(input_text: str) -> str:
    """Text basic preprocessing.

    Lowercase, leave only russian/english letters, remove basic stopwords.

    Args:
        input_text (str): input text for processing.

    Returns:
        str: processed text
    """
    text = input_text.lower()  # приведение к нижнему регистру
    text = re.sub(
        r"https?://\S+|www\.\S+|\[.*?\]|[^a-zA-Z\s]+|\w*\d\w*", "", text
    )  # убираем ссылки
    text = re.sub("[0-9 \-_]+", " ", text)  # убираем спец символы
    text = re.sub("[^a-z A-Z]+", " ", text)  # оставляем только буквы
    text = " ".join(  # убираем стоп слова
        [word for word in text.split() if word not in stopwords.words("english")]
    )
    return text.strip()


class CleanText(Task):
    """Remove basic stopwords, lowercase words."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(CleanText, self).__init__(*args, **kwargs)
        self.output_path = self.task_dict_config["clean_text_file"]

    def requires(self) -> Task:
        pass

    def run(self) -> None:
        data_frame = pl.read_csv(self.task_dict_config["raw_file"])
        data_frame.columns = ["Polarity", "Title", "Review"]

        data_frame = data_frame.select("Polarity", "Review").with_columns(
            pl.col("Polarity").map_elements(
                lambda polarity: "Negative" if polarity == 1 else "Positive"
            )
        )

        cleaned_dataframe = data_frame.with_columns(
            pl.col("Review").map_elements(basic_clean).str.split(" ").alias("corpus")
        )
        cleaned_dataframe.write_parquet(self.output_path)

    def output(self) -> LocalTarget:
        return LocalTarget(self.output_path)


class LemmatizeWords(Task):
    """Lemmatize all the tokens."""

    task_dict_config = DictParameter()

    def __init__(self, *args, **kwargs):
        super(LemmatizeWords, self).__init__(*args, **kwargs)
        self.output_path = self.task_dict_config["lemmatized_file"]

    def requires(self) -> Task:
        return CleanText(self.task_dict_config)

    def run(self) -> None:
        input_frame = pl.read_parquet(self.requires().output().path)

        lemmatizer = WordNetLemmatizer()
        lemmatized_words = input_frame.with_columns(
            pl.col("corpus").map_elements(
                lambda input_list: [lemmatizer.lemmatize(token) for token in input_list]
            )
        )

        lemmatized_words.write_parquet(self.output_path)

    def output(self) -> LocalTarget:
        return LocalTarget(self.output_path)
