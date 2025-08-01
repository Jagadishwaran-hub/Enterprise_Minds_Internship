# src/services/llm_service.py

import groq
import requests
from typing import Dict, Any

class LLMService:
    def __init__(self):
        self.model_name = "llama3-8b-8192"
        self.api_key = self._get_api_key()
        self.client = None

    def _get_api_key(self) -> str:
        """Return the Groq API key"""
        return ""

    def initialize(self):
        try:
            print("Initializing Groq client...")
            self.client = groq.Groq(api_key=self.api_key)
            print("Groq client initialized successfully!")
        except Exception as e:
            print(f"Error initializing Groq client: {e}")
            raise

    def generate_answer(self, question: str, context: str) -> str:
        try:
            if self.client is None:
                self.initialize()

            prompt = f"""Based on the following context, please answer the question.

Context: {context}

Question: {question}

Answer:"""

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Let's have a casual conversation. Reply naturally like you're chatting with a friend."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=512
            )

            return response.choices[0].message.content.strip()

        except Exception as groq_error:
            print(f"Groq client error: {groq_error}")
            return self._call_groq_api_directly(prompt)

    def _call_groq_api_directly(self, prompt: str) -> str:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Let's have a casual conversation. Reply naturally like you're chatting with a friend."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            print(f"Direct API call error: {e}")
            return f"I apologize, but I encountered an error while generating the answer: {str(e)}"

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "device": "Groq Cloud",
            "is_loaded": self.client is not None,
            "model_type": "Llama 3-8B-8192 (Groq)"
        }
