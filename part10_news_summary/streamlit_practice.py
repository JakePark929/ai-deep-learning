import streamlit as st

st.title("첫번째 데모입니다.")
st.header("이것은 헤더입니다.")
st.subheader("이것은 서브헤더입니다.")
st.text("이것은 텍스트입니다.")
st.markdown("***이것은 마크다운입니다.***")
st.code("print('Hello, World!')", language="python")

# 입력컴포넌트
name = st.text_input("이름을 입력하세요.")
age = st.number_input("나이를 입력하세요.", min_value=0, max_value=120, value=20)

st.write(f"이름: {name}, 나이: {age}")

# 버튼
if st.button("확인"):
    st.write("확인되었습니다.")
else:
    st.write("취소되었습니다.")