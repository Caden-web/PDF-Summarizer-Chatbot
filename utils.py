import PyPDF2
from openai import OpenAI

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def get_summary(text, api_key):
    client = OpenAI(api_key=api_key)
    prompt = f"""
    Summarize the following text in one concise paragraph:
    ```{text}```
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content

def ask_question(chat_history, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0.7,
    )
    return response.choices[0].message.content
