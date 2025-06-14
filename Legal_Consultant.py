import streamlit as st
import openai

# Initialize OpenAI with your secret API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("⚖️ Legal Consultant Bot")

# Initialize chat history with a legal-domain system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI assistant specialized in legal advice and consultation. "
                "You provide general legal information and help users understand legal topics and terms. "
                "You are not a licensed attorney and cannot give specific legal opinions or represent clients. "
                "If the user asks about medical, technical, or unrelated topics, respond with: "
                "'I'm here to help with legal questions only. Please ask about legal issues, rights, contracts, or related topics.' "
                "If a user describes a legal emergency or complex case, advise: "
                "'This may require professional legal assistance. Please consult a licensed attorney or legal service provider.'"
            )
        }
    ]

# Display all previous messages (except system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your legal question...")

# Function to get AI response
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

# Process user input
if user_input:
    # Add user's message to history and show
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response = get_response(st.session_state.messages)
    
    # Add assistant response to history and show
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Optional: Legal Disclaimer Footer
st.markdown("---")
st.markdown(
    "📌 **Disclaimer:** This chatbot provides general legal information only and does not constitute legal advice. "
    "Always consult a qualified lawyer for advice on your specific situation.",
    unsafe_allow_html=True
)