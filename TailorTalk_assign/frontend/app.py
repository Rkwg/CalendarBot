import streamlit as st
import requests

st.title("📅 AI Calendar Booking Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask to book a meeting...")

if user_input:
    response = requests.post("https://calendarbot-1660.onrender.com/message", json={"text": user_input})
    # bot_reply = response.json()["reply"]
    try:
        json_data = response.json()
        bot_reply = json_data["reply"]
    except Exception as e:
        st.error("⚠️ Backend error or invalid response:")
        st.code(response.text)
        # raise e
        bot_reply = "⚠️ Internal error. Please check logs or try again."

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("agent", bot_reply))

for sender, msg in st.session_state.messages:
    with st.chat_message(sender):
        st.markdown(msg)

