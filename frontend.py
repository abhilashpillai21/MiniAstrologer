import streamlit as st
import random
import time

st.title(":rainbow[Mini Astrology App]")

uploaded_file = st.file_uploader("Upload your birthcharts as txt", type="txt")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant", "content":"Ask your question"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:= st.chat_input("Ask your question"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = random.choice(["Try again!",
                      "Trying to fetch answers",
                      "We are facing downtime."])
        st.session_state.messages.append({"role":"assistant", "content":full_response})
        message_placeholder.markdown(full_response)    


def getuploadfile():
    return uploaded_file