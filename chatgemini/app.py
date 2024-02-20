import streamlit as st
import google.generativeai as genai

from clients.secret_manager import SecretManagerClient


class ChatApp:
    def __init__(self):
        self.secret_manager_client = SecretManagerClient()
        api_key = self.secret_manager_client.access_secret_version("AI_STUDIO_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        with st.sidebar:
            self.candidate_count = st.number_input("# of responses")
            self.stop_sequences = st.multiselect(
                "Stop sequences",
                ["."],
            )
            self.max_output_tokens = st.number_input("Maximum length")
            self.top_p = st.number_input("Top P")
            self.top_k = st.number_input("Top K")
            self.temperature = st.slider("Temperature", 0.0, 1.0, 0.1)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me Anything"}
            ]

    def run(self):
        st.title("ChatGemini")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        query = st.chat_input("Message ChatGemini...")

        if query:
            with st.chat_message("user"):
                st.markdown(query)

            self.process_query(query)

    def process_query(self, query):
        try:
            response = self.model.generate_content(
                query,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    stop_sequences=self.stop_sequences,
                    max_output_tokens=self.max_output_tokens,
                    top_p=self.top_p,
                    top_k=self.top_k,
                    temperature=self.temperature,
                ),
            )

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
