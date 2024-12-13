import streamlit as st
from service.research_service import ResearchService

# 세션 상태에 'research_service' 객체가 없으면 한 번만 생성
if "research_service" not in st.session_state:
    st.session_state.research_service = ResearchService()

### Client 구현 ###
st.title("🧑‍🔬Wisebot: AI Research Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 메시지들 출력
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 사용자 입력을 받아 처리
if prompt := st.chat_input("궁금한 점을 물어보세요."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 저장된 research_service 객체를 사용하여 응답 생성
    response = f"bot: {st.session_state.research_service.prompt_and_generate(prompt.strip())}"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})