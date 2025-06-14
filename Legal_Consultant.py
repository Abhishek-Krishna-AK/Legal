import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set Streamlit app title
st.title("Legal Advisor ChatBot")

# Initialize chat history with a legal-only system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional legal assistant. "
                "Only provide legal advice or consultation. "
                "If asked about non-legal topics, respond with: "
                "'I'm only able to assist with legal matters. Please ask a legal-related question.'"
            )
        }
    ]

# Display past messages
for msg in st.session_state.messages[1:]:  # skip system message in display
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box for user
user_input = st.chat_input("Ask your legal question...")

# (Optional) Guardrail keywords – you can expand this list
restricted_keywords = ['movie', 'weather', 'food', 'cooking', 'sports', 'travel', 'music']

# Define function to get assistant's response
def get_response(history):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    return response.choices[0].message.content

# Handle user input
if user_input:
    if any(word in user_input.lower() for word in restricted_keywords):
        st.warning("⚠️ This chatbot is for legal advice only. Please ask a legal-related question.")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get and display assistant response
        response = get_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)