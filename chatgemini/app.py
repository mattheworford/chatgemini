import os
import google.generativeai as genai

from secret_manager import SecretManagerClient

secret_manager_client = SecretManagerClient()
api_key = secret_manager_client.access_secret_version("AI_STUDIO_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("List 5 planets each with an interesting fact")
print(response.text)

response = model.generate_content("what are top 5 frequently used emojis?")
print(response.text)
