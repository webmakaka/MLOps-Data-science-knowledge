import polars as pl
import nltk
from pathlib import Path

if __name__ == "__main__":
    nltk.download('wordnet')
    amazon_root = Path('Amazon reviews')
    dataframe_50k = pl.read_csv(amazon_root / 'train.csv', n_rows=50000)
    dataframe_50k.write_csv("data/raw/train_50k.csv")
