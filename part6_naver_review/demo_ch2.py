import pandas as pd
import streamlit as st
from ch02.inference import inference_json

url = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt"
df = pd.read_csv(url, sep="\t")
review = st.selectbox('리뷰', df.iloc[:10]['document'])

if st.button("submit"):
    score = inference_json(review)
    st.write(score)