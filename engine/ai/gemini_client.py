import os

from google import genai


class GeminiClient:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not self.api_key:
            raise Exception(
                "Missing GEMINI_API_KEY"
            )

        self.client = genai.Client(
            api_key=self.api_key
        )


    def generate(
        self,
        prompt: str,
        model="gemini-3.5-flash-lite"
    ):

        try:

            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )

            if not response.text:

                return (
                    "GEMINI_ERROR: "
                    "Empty response"
                )

            return response.text


        except Exception as exc:

            return (
                "GEMINI_ERROR: "
                + str(exc)
            )
