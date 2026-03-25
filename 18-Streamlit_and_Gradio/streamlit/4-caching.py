from time import sleep

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(persist="disk")  # если persist=False - то хранится в RAM
def transform(df: pd.DataFrame):
    sleep(5)
    df = df.filter(items=["one", "three"])
    df = df.apply(np.sum, axis=0)
    return df


my_df = pd.DataFrame(
    np.array(([1, 2, 3], [4, 5, 6])),
    columns=["one", "two", "three"],
)

st.write(transform(my_df))
st.radio("rerun", options=["Тык", "Тык"])
