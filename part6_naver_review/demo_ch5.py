import pandas as pd
import streamlit as st

from ch05.inference import inference_all

url = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt"
df = pd.read_csv(url, sep='\t')
data = df.iloc[:10].to_dict(orient="records")
options = {item["document"]: item for item in data}
reviews = st.multiselect("리뷰", options.keys())
if st.button("submit"):
    selected_values = [options[doc] for doc in reviews]
    result = inference_all(selected_values)
    st.json(result)