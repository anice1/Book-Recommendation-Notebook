import streamlit as st
import pandas as pd
from Recommender import Recommend

rc = Recommend()


st.title('Book Recommender')

col1, col2, col3, col4, col5 = st.beta_columns(5)

book_name = st.text_input('Enter Book Name')
check = st.button('Recommend')
if check:
    st.dataframe(rc.recommend(book_name))