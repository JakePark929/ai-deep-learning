import os
import pickle

from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from search_and_answer import search, generate_answer

load_dotenv()
INDEX_PATH = os.getenv("INDEX_PATH")
directory = INDEX_PATH

with open(f"{directory}/qas.pkl", "rb") as f:
    qas = pickle.load(f)

df = pd.DataFrame(qas)
st.dataframe(df)

question = st.text_input("질문", "이벤트 언제까지에요?")
if st.button("Submit"):
    qa = search(question)
    answer = generate_answer(qa, question)
    st.write(answer)