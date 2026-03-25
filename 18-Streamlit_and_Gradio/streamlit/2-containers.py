import streamlit as st

my_container = st.container()

st.write("a")  # --- 3
st.write("b")  # --- 4

my_container.write("Inside container")  # --- 1
my_container.write("Also inside container")  # --- 2
