import os
from dotenv import load_dotenv
load_dotenv()

import json
import os
from groq import Groq
from app.prompt.prompt_registry import get_system_prompt

print("MODEL FROM ENV AT RUNTIME:", os.getenv("GROQ_MODEL"))

class AIEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def build_messages(self, underwriting_context):
        """
        Build the message payload for the LLM using the dynamic system prompt
        selected by the Prompt Orchestrator.
        """
        system_prompt = get_system_prompt(underwriting_context)

        return [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": "Use the following underwriting context to generate AI insights."
            },
            {
                "role": "user",
                "content": json.dumps(underwriting_context)
            }
        ]

    def generate_insights(self, underwriting_context):
        """
        Calls Groq LLM with the dynamically selected prompt and underwriting context.
        Returns the raw model output string.
        """
        messages = self.build_messages(underwriting_context)

        response = self.client.chat.completions.create( 
            model=os.getenv("GROQ_MODEL"), 
            messages=messages, 
            temperature=0.0 
        )

        return response.choices[0].message.content

