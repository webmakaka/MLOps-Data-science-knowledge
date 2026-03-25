def prepare_train_test_split(
        input_path,
        output_path,
        random_state,
        train_path,
        test_path
    ):
    """Split input files into train and test groups."""
    import polars as pl
    from sklearn.model_selection import train_test_split
    input_frame = pl.read_parquet(input_path)

    train, test = train_test_split(
        input_frame,
        test_size=0.3,
        shuffle=True,
        random_state=random_state,
    )

    train.write_parquet(train_path)
    test.write_parquet(test_path)
