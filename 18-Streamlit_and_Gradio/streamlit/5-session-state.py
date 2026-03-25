import streamlit as st

# ----------------------------------------------------------------

if "my_slider" not in st.session_state:
    st.session_state.my_slider = 8

st.slider(
    "Slider",  # при ререндеринге значение слайдера устанавливается = 8
    min_value=0,
    max_value=20,
    key="my_slider",  # key совпадает с записанным ранее ключом в словарь session-state
)

# ----------------------------------------------------------------


# callback on change
def my_callback():
    st.session_state["nice-key"] = "awesome-value"


checkbox_input = st.checkbox("Yes or No", key="checkbox-key", on_change=my_callback)

# ----------------------------------------------------------------


# посмотрим что получилось
st.write(st.session_state)
