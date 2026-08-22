import os
import re

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


    @staticmethod
    def clean_response(
        content
    ):

        if not content:
            return ""

        content = str(
            content
        )

        # Entfernt interne Reasoning-Blöcke
        content = re.sub(
            r"<think>.*?</think>",
            "",
            content,
            flags=re.DOTALL | re.IGNORECASE
        )

        return content.strip()


    def generate(
        self,
        prompt: str,
        model="qwen/qwen3.6-27b"
    ):

        try:

            response = (
                self.client
                .chat
                .completions
                .create(

                    model=model,

                    messages=[
                        {
                            "role": "system",
                            "content":
                                (
                                    "Du bist ein schneller Analyse-Agent "
                                    "im Free Basics AI Marketing System. "
                                    "Gib nur die angeforderte Antwort aus. "
                                    "Keine internen Gedankengänge."
                                )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.2
                )
            )


            content = (
                response
                .choices[0]
                .message
                .content
            )


            content = self.clean_response(
                content
            )


            if not content:

                return (
                    "GROQ_ERROR: "
                    "Empty response"
                )


            return content


        except Exception as exc:

            return (
                "GROQ_ERROR: "
                + str(exc)
            )
