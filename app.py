import streamlit as st
import pandas as pd

st.title("DataWIZ")
st.write("Welcome to my Data Analysis App!")

uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
