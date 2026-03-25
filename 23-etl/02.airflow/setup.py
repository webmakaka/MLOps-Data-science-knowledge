import polars as pl
from pathlib import Path
from datetime import datetime, timedelta

if __name__ == "__main__":
    current_date = datetime.today()
    start_date = (current_date - timedelta(days=2)).strftime('%Y%m%d')
    next_execution_date = (current_date - timedelta(days=1)).strftime('%Y%m%d')
    amazon_root = Path('Amazon reviews')
    dataframe_50k = pl.read_csv(amazon_root / 'train.csv', n_rows=50000)
    dataframe_50k.write_csv(f"dags/data/raw/train_{start_date}.csv")

    dataframe_100k = pl.read_csv(amazon_root / 'train.csv', n_rows=100000)
    dataframe_100k.write_csv(f"dags/data/raw/train_{next_execution_date}.csv")
