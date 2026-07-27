import os
import requests


class PerplexityClient:


    def __init__(self):

        self.api_key = os.environ.get(
            "PERPLEXITY_API_KEY"
        )

        self.url = (
            "https://api.perplexity.ai/chat/completions"
        )


    def generate(self, prompt):

        if not self.api_key:
            return (
                "PERPLEXITY_ERROR: "
                "Missing API Key"
            )


        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json"

        }


        payload = {

            "model":
                "sonar",

            "messages":[

                {

                    "role":
                        "system",

                    "content":
                        "Du bist ein Faktenprüfer."

                },

                {

                    "role":
                        "user",

                    "content":
                        prompt

                }

            ]

        }


        try:

            response = requests.post(

                self.url,

                headers=headers,

                json=payload,

                timeout=60

            )


            data = response.json()


            return (
                data
                .get("choices",[{}])[0]
                .get("message",{})
                .get("content","")
            )


        except Exception as e:

            return (
                f"PERPLEXITY_ERROR: {e}"
            )
