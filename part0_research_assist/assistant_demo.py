import streamlit as st

from service.research_service import ResearchService

research_service = ResearchService()

### Client 구현 ###
st.title("🧑‍🔬Wisebot: AI Research Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("궁금한 점을 물어보세요."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"bot: {research_service.prompt_and_generate(prompt.strip())}"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})