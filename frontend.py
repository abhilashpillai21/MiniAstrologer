import streamlit as st
import random
import time
import vectordb
#import analysecharts

def getuploadfile():
    if uploaded_file is not None:
        uploaded_file.seek(0)
        return uploaded_file.read().decode("utf-8")  
    return None

def getuploadedfilename():
    if uploaded_file is not None:
        return uploaded_file.name 
    return None

def getquestion():
    return st.session_state.messages[-1]["content"] if "messages" in st.session_state else ""

st.title(":rainbow[Mini Astrology App]")

uploaded_file = st.file_uploader("Upload your birthcharts as txt", type="txt", key="main_file_uploader")

if uploaded_file is not None:
    if "last_file" not in st.session_state or st.session_state.last_file!=uploaded_file.name:
        st.session_state.embeddings = None
        st.session_state.last_file = uploaded_file.name

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
        file_text = getuploadfile()
        #full_response, sources = analysecharts.findanswers(file_text, prompt)
        if file_text is None:
            full_response="Please add a file first"
            sources = []    
        else:    
            full_response, sources = vectordb.findanswers(file_text, prompt)
        st.session_state.messages.append({"role":"assistant", "content":full_response})
        message_placeholder.markdown(full_response)    

        with st.sidebar:    
            with st.expander("Sources used"):
                for score, text in sources: 
                    st.markdown(f"**Score : ** {score:.4f}")
                    st.code(text)


