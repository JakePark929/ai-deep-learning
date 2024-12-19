import streamlit as st
from ch02.inference import inference_json

review = st.text_input('리뷰', "이 영화 재밌어요~")
if st.button("submit"):
    score = inference_json(review)
    st.write(score)