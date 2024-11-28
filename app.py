import streamlit as st
from dotenv import load_dotenv 
load_dotenv() #load all environment variables

import os
import google.generativeai as genai
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


from markdown_it import MarkdownIt  # Import Markdown parser
import re

def strip_formatting(markdown_text):
    """
    Removes simple Markdown formatting using regex.
    """
    return re.sub(r"(\*\*|\*|`|_|~)", "", markdown_text)


def generate_gemini_content(transcript_text, prompt):
    """
    Generate content using the Gemini model.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

# Streamlit page configuration
st.set_page_config(page_title="Personal E-Shopping Assistant")

# Sidebar configuration
with st.sidebar:
    st.title('Personal E-Shopping Assistant')
    st.write('This chatbot analyzes product reviews to help answer queries about products.')
    st.success('Ready to assist with your shopping queries!', icon='✅')
    st.subheader('Controls')
    if st.button('Clear Chat History'):
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.experimental_rerun()

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages in a conversational format
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if user_query := st.chat_input("Ask your shopping-related questions here..."):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # Generate and display assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Using Gemini model to generate response
            prompt = "You are a helpful e-shopping assistant.Provide detailed and helpful responses.If anything related to cost or price, mention the price. If anything related to product specs, give in detail. If asked for reviews , give both negative aspects and positive aspects. "
            raw_response = generate_gemini_content(user_query, prompt)
            plain_response = strip_formatting(raw_response)  # Remove formatting
            placeholder = st.empty()
            placeholder.write(plain_response)  # Display plain text
        st.session_state.messages.append({"role": "assistant", "content": plain_response})

