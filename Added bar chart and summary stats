import streamlit as st
import pandas as pd

st.title("DataWIZ")
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Tera Data:", df)
    
    st.bar_chart(df,x="Name",y="Marks")  
    st.write("Summary:", df.describe()) 
