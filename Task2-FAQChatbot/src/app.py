import streamlit as st

from chatbot import FAQChatbot


# Page configuration
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="💬",
    layout="centered"
)


# Load chatbot
@st.cache_resource
def load_chatbot():
    return FAQChatbot(threshold=0.20)


chatbot = load_chatbot()


# Page title
st.title("💬 FAQ Chatbot")
st.write(
    "Ask a question and the chatbot will find "
    "the most relevant answer from the FAQ knowledge base."
)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and "score" in message:
            st.caption(
                f"Similarity score: {message['score']:.2f}"
            )


# Chat input
user_question = st.chat_input("Type your question here...")


if user_question:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Get chatbot response
    result = chatbot.get_response(user_question)

    # Add assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "score": result["score"]
        }
    )

    # Refresh page to display messages
    st.rerun()