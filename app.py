import streamlit as st
from utils import extract_text_from_pdf, get_summary, ask_question

st.set_page_config(page_title="PDF Summarizer Chatbot", layout="centered")

st.title("📄 PDF Summarizer W/ Chatbot")

# Step 1: API Key
api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
if not api_key:
    st.warning("Please enter your OpenAI API key or get one here: https://platform.openai.com/api-keys")
    st.stop()

# Step 2: Upload PDF
uploaded_pdf = st.file_uploader("📤 Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    with st.spinner("Extracting and summarizing..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        summary = get_summary(pdf_text, api_key)
    
    st.subheader("📋 Summary")
    st.info(summary)

    # Step 3: Chatbot
    st.subheader("💬 Ask questions about the summary")
    chat_history = [
        {"role": "system", "content": f"You're a helpful assistant. Answer questions based on this summary:\n{summary}"}
    ]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = chat_history

    user_input = st.text_input("Ask your question:")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = ask_question(st.session_state.chat_history, api_key)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        st.write(f"**Bot:** {response}")
