def train_tfidf_logistic_regression_model(
    input_vectorizer,
    train_frame,
    random_state,
    multi_class,
    solver,
    output_path
):
    """Train log reg on tfidf features."""
    import pickle
    import polars as pl
    from sklearn.linear_model import LogisticRegression

    with open(input_vectorizer, "rb") as input_vectorizer:
        vectorizer = pickle.load(input_vectorizer)

        train_frame = pl.read_parquet(train_frame)
        train_features = vectorizer.transform(
            train_frame["corpus"].to_pandas().astype(str)
        )

        model_log_reg = LogisticRegression(
            random_state=random_state,
            multi_class=multi_class,
            solver=solver,
        )

        model_log_reg.fit(train_features, train_frame["Polarity"])
        with open(output_path, "wb") as output_model_file:
            pickle.dump(model_log_reg, output_model_file)
