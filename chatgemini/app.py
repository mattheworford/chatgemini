import streamlit as st
import google.generativeai as genai

from clients.secret_manager import SecretManagerClient


class ChatApp:
    def __init__(self):
        self.secret_manager_client = SecretManagerClient()
        self.api_key = self.secret_manager_client.access_secret_version(
            "AI_STUDIO_API_KEY"
        )
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me Anything"}
            ]

    def run(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("What's up?")

        if query:
            with st.chat_message("user"):
                st.markdown(query)

            self.process_query(query)

    def process_query(self, query):
        try:
            response = self.model.generate_content(query)

            with st.chat_message("assistant"):
                st.markdown(response.text)

            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append(
                {"role": "assistant", "content": response.text}
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


chat_app = ChatApp()
chat_app.run()
