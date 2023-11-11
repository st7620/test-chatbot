import streamlit as st
#from transformers import pipeline
from docquery import document, pipeline

# App title
st.set_page_config(page_title="Document Chatbot")

# File uploader widget  
doc = document.load_document(st.file_uploader("Choose a file"))

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating response
def generate_response(uploaded_file, prompt_input):                       
    p = pipeline("document-question-answering")
    #doc = document.load_document(uploaded_file)
    return p(question=prompt_input, **doc.context)[0]["answer"]

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(uploaded_file, prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)