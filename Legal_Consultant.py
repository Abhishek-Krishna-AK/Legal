
✅ Streamlit Legal Consultant Chatbot Code
python
Copy
Edit
import streamlit as st
import openai

# Initialize OpenAI with your secret API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("⚖️ Legal Consultant Chatbot")

# Initialize chat history with a legal-only system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional legal assistant. "
                "You only provide help related to legal matters such as contracts, disputes, property law, consumer rights, etc. "
                "Do not offer advice on non-legal topics. "
                "If a user asks a non-legal question, respond with: "
                "'I'm here to help with legal matters only. Please ask a legal-related question.' "
                "Also, clearly state that you are not a lawyer and this is not official legal advice. "
                "For serious legal matters, recommend contacting a licensed attorney."
            )
        }
    ]

# Display previous conversation (excluding system message)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input for user's legal query
user_input = st.chat_input("Describe your legal issue...")

# Function to get OpenAI assistant response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Process user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_response(st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Footer disclaimer
st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This chatbot is not a licensed attorney and does not offer legal representation. "
    "It provides general information only. For legal advice, consult a qualified legal professional.",
    unsafe_allow_html=True
)