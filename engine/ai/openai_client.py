import os
from openai import OpenAI


class OpenAIClient:

    def __init__(self):

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not self.api_key:
            raise Exception(
                "Missing OPENAI_API_KEY"
            )

        self.client = OpenAI(
            api_key=self.api_key
        )


    def generate(
        self,
        prompt: str,
        model="gpt-4.1-mini"
    ):

        response = self.client.chat.completions.create(

            model=model,

            messages=[
                {
                    "role": "system",
                    "content":
                    "Du bist ein Analyse-Agent im Free Basics AI Marketing System."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        return response.choices[0].message.content
