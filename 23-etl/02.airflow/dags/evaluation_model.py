def conf_matrix(y_true, pred):
    from matplotlib import pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay
    plt.ioff()
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, pred, ax=ax, colorbar=False)
    ax.xaxis.set_tick_params(rotation=90)
    _ = ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


def evaluate_tfidf_model(
        input_model,
        input_vectorizer,
        test_path,
        report_file_path,
        conf_matrix_path
):
    import json
    import pickle
    import polars as pl
    from matplotlib import pyplot as plt
    from sklearn.metrics import classification_report

    with open(input_model, "rb") as input_model:
        model_log_reg = pickle.load(input_model)

    with open(input_vectorizer, "rb") as input_vectorizer:
        vectorizer = pickle.load(input_vectorizer)

    test_frame = pl.read_parquet(test_path)
    test_features = vectorizer.transform(
        test_frame["corpus"].to_pandas().astype(str)
    )

    predicts = model_log_reg.predict(test_features)
    report = classification_report(
        test_frame["Polarity"], predicts, output_dict=True
    )
    with open(report_file_path, "w") as report_file:
        json.dump(report, report_file, indent=4)

    confusion_matrix_fig = conf_matrix(test_frame["Polarity"], predicts)

    confusion_matrix_fig.figure.savefig(
        conf_matrix_path,
        transparent=False,
        facecolor="white",
        bbox_inches="tight",
    )
    plt.close(confusion_matrix_fig)
