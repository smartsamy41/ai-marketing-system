from pathlib import Path
import json


BASE = Path("public_web_assets/datasets")


def replace_urls(file):

    path = BASE / file

    data = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


    def clean(obj):

        if isinstance(obj, dict):

            for key, value in obj.items():

                if isinstance(value, str):

                    if "/lp/" in value:

                        obj[key] = (
                            value
                            .replace(
                                "/lp/",
                                "/angebote/"
                            )
                        )

                else:
                    clean(value)


        elif isinstance(obj, list):

            for item in obj:
                clean(item)


    clean(data)


    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


replace_urls(
    "verified-products.json"
)

replace_urls(
    "verified-products.jsonld"
)


print(
    "FINAL PUBLIC ROUTE REPLACEMENT DONE"
)
