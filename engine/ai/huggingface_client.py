import os

from openai import OpenAI


class HuggingFaceClient:

    def __init__(self):

        self.api_key = os.getenv(
            "HF_TOKEN"
        )

        if not self.api_key:

            raise Exception(
                "Missing HF_TOKEN"
            )


        self.client = OpenAI(

            base_url=
                "https://router.huggingface.co/v1",

            api_key=
                self.api_key

        )


    def generate(
        self,
        prompt: str,
        model="openai/gpt-oss-120b:preferred"
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
                            "role":
                                "system",

                            "content":
                                (
                                    "Du bist ein Open-Source-"
                                    "Analyse-Agent im Free Basics "
                                    "AI Marketing System."
                                )
                        },
                        {
                            "role":
                                "user",

                            "content":
                                prompt
                        }
                    ],

                    temperature=0.2
                )
            )


            return (
                response
                .choices[0]
                .message
                .content
            )


        except Exception as exc:

            return (
                "HUGGINGFACE_ERROR: "
                + str(exc)
            )
