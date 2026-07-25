from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:

    def __init__(
        self,
        template_path="templates"
    ):
        self.env = Environment(
            loader=FileSystemLoader(template_path)
        )

    def render(
        self,
        template_name,
        data
    ):

        template = self.env.get_template(
            template_name
        )

        return template.render(
            **data
        )


if __name__ == "__main__":

    renderer = TemplateRenderer()

    html = renderer.render(
        "landingpages/geo_optimized_landingpage.html",
        {
            "title": "Strom Vergleich",
            "description": "Informationen zu Stromtarifen",
            "canonical_url": "https://freebasics.online/lp/CHK24_001",
            "schema_json": "{}",
            "product_id": "CHK24_001",
            "category": "Energie",
            "partner": "check24",
            "tracking_url": "#",
            "content": "Test Inhalt"
        }
    )

    print(html[:500])
