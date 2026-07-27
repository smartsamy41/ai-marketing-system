import os

from groq import Groq


class GroqClient:

    def __init__(self):

        self.api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not self.api_key:
            raise Exception(
                "Missing GROQ_API_KEY"
            )

        self.client = Groq(
            api_key=self.api_key
        )


    def generate(
        self,
        prompt: str,
        model="llama-3.1-8b-instant"
    ):

        response = self.client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "system",
                    "content":
                    "Du bist ein schneller Analyse-Agent im Free Basics AI System."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        return response.choices[0].message.content
