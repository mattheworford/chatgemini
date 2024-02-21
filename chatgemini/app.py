import streamlit as st
import google.generativeai as genai

from clients.secret_manager import SecretManagerClient

HARM_CATEGORIES = [
    "HARM_CATEGORY_DANGEROUS",
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
]


class ChatApp:
    def __init__(self):
        self.secret_manager_client = SecretManagerClient()
        self.configure_genai()
        self.model = genai.GenerativeModel("gemini-pro")
        self.initialize_session_state()
        self.initialize_sidebar()

    def configure_genai(self):
        api_key = self.secret_manager_client.access_secret_version("AI_STUDIO_API_KEY")
        genai.configure(api_key=api_key)

    def initialize_session_state(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Ask me Anything"}
            ]

    def initialize_sidebar(self):
        with st.sidebar:
            self.candidate_count = int(
                st.number_input("# of responses", step=1, value=1)
            )
            self.stop_sequences = st.multiselect(
                "Stop sequences", ["."], placeholder="Select"
            )
            self.max_output_tokens = int(
                st.number_input("Maximum length", step=1, value=100)
            )
            self.nucleus_sampling_enabled = st.toggle("Nucleus sampling")
            self.top_p = st.number_input(
                "Top P",
                step=0.1,
                value=1.0,
                disabled=not self.nucleus_sampling_enabled,
            )
            self.top_k_sampling_enabled = st.toggle("Top-K sampling")
            self.top_k = int(
                st.number_input(
                    "Top K",
                    step=1,
                    value=100,
                    disabled=not self.top_k_sampling_enabled,
                )
            )
            self.temperature = st.slider("Temperature", 0.0, 1.0, 0.1)

    def run(self):
        st.title("ChatGemini")
        self.display_messages()
        query = st.chat_input("Message ChatGemini...")
        if query:
            with st.chat_message("user"):
                st.markdown(query)
            self.process_query(query)

    def display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def process_query(self, query):
        try:
            response = self.model.generate_content(
                query,
                generation_config=self.get_generation_config(),
                safety_settings=self.get_safety_settings(),
            )
            self.handle_response(response, query)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    def get_generation_config(self):
        return genai.types.GenerationConfig(
            candidate_count=self.candidate_count,
            stop_sequences=(
                self.stop_sequences if len(self.stop_sequences) > 0 else None
            ),
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p if self.nucleus_sampling_enabled else None,
            top_k=self.top_k if self.top_k_sampling_enabled else None,
            temperature=self.temperature,
        )

    def get_safety_settings(self):
        return [
            {"category": category, "threshold": "BLOCK_NONE"}
            for category in HARM_CATEGORIES
        ]

    def handle_response(self, response, query):
        st.session_state.messages.append({"role": "user", "content": query})
        try:
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
        except:
            for candidate in response.candidates:
                with st.chat_message("assistant"):
                    for part in candidate.content.parts:
                        st.markdown(part.text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": part.text}
                        )


chat_app = ChatApp()
chat_app.run()
