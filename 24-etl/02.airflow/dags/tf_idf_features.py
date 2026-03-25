def train_tfidf_vectorizer(input_path, output_path, analyzer, max_features):
    """Train vectorizers on train/test splits."""
    import pickle
    import polars as pl
    from sklearn.feature_extraction.text import TfidfVectorizer
    train_frame = pl.read_parquet(input_path)
    tfidf_vectorizer = TfidfVectorizer(
        analyzer=analyzer,
        max_features=max_features,
    )

    tfidf_vectorizer.fit(train_frame["corpus"].to_pandas().astype(str))
    with open(output_path, "wb") as output:
        pickle.dump(tfidf_vectorizer, output)
