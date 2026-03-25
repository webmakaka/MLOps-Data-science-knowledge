import os

import pandas as pd
import streamlit as st

st.title("Hello from Streamlit")

df = pd.read_csv(
    os.environ.get("SALES_FILEPATH"),
)

st.dataframe(df.sample(5))
