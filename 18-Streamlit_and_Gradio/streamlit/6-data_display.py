import numpy as np
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    {
        "first": [1, 2, 3, 4],
        "second": [40, 20, 30, 10],
    }
)

# два эквивалентных варианта
st.write(df)
st.dataframe(df)

# статическая таблица
st.table(df)

# можно передавать любой Iterable
st.dataframe([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])

# -----------------
st.divider()  # ---
# -----------------


# линейный график - тоже можно просто передать любой Iterable...
st.line_chart([1, 2, 4, 7])

# ...или таблицу
chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["a", "b"])
st.line_chart(chart_data)

st.line_chart(chart_data, x="a", y="b")

# -----------------
st.divider()  # ---
# -----------------

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [59.93, 30.31], columns=["lat", "lon"]
)

st.map(map_data, color="#88c2a8")
