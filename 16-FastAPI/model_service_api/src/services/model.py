from transformers import pipeline


class EmotionClassifier:
    """
    Классификатор эмоций на основе предобученной модели Transformers.

    Methods:
        predict_emotion: Предсказание эмоций по тексту.
    """

    model = pipeline(model="seara/rubert-tiny2-ru-go-emotions")

    @classmethod
    def predict_emotion(cls, text: str):
        """
        Предсказание эмоций по тексту.

        Args:
            text (str): Текст для анализа эмоций.

        Returns:
            dict: Результат предсказания в формате словаря.
        """
        result = cls.model(text)
        return result
