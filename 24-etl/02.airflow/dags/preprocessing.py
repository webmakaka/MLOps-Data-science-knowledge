def download_stopwords():
    import nltk
    nltk.download('stopwords')


def basic_clean(input_text: str) -> str:
    import re
    from nltk.corpus import stopwords
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


def clean_text_task(raw_file, output_path):
    import polars as pl
    import logging

    logging.info(f"{output_path}")

    data_frame = pl.read_csv(raw_file)
    data_frame.columns = ["Polarity", "Title", "Review"]

    data_frame = data_frame.select("Polarity", "Review").with_columns(
        pl.col("Polarity").map_elements(
            lambda polarity: "Negative" if polarity == 1 else "Positive"
        )
    )

    cleaned_dataframe = data_frame.with_columns(
        pl.col("Review").map_elements(basic_clean).str.split(" ").alias("corpus")
    )
    cleaned_dataframe.write_parquet(output_path)


def lemmatize_words(input_path, output_path):
    """Lemmatize all the tokens."""
    import polars as pl
    import nltk
    from nltk.stem import WordNetLemmatizer

    input_frame = pl.read_parquet(input_path)
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = input_frame.with_columns(
        pl.col("corpus").map_elements(
            lambda input_list: [lemmatizer.lemmatize(token) for token in input_list]
        )
    )

    lemmatized_words.write_parquet(output_path)
