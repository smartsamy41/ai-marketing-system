import json
from pathlib import Path


class GeoProductMatcher:

    def __init__(self):

        self.category_map_file = Path(
            "data_master/linking/category_map.json"
        )

        self.product_master_file = Path(
            "data_master/catalog/product_master_44.json"
        )

        self.geo_rules_file = Path(
            "data_master/geo_layer/geo_content_rules.json"
        )


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)


    @staticmethod
    def clean(value):

        if value is None:
            return ""

        return str(value).strip()


    @staticmethod
    def normalize(value):

        return (
            str(value or "")
            .strip()
            .lower()
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )


    def find_product(self, product_id):

        data = self.load_json(
            self.product_master_file
        )

        for product in data.get(
            "products",
            []
        ):

            if self.clean(
                product.get("product_id")
            ) == self.clean(product_id):

                return product

        return {}


    def find_category_mapping(
        self,
        product_id,
        category
    ):

        data = self.load_json(
            self.category_map_file
        )

        category_normalized = self.normalize(
            category
        )

        for key, mapping in data.get(
            "categories",
            {}
        ).items():

            ids = []

            if mapping.get("product_id"):

                ids.append(
                    mapping.get("product_id")
                )

            ids.extend(
                mapping.get(
                    "product_ids",
                    []
                )
                or []
            )


            if (
                product_id in ids
                and self.normalize(key)
                == category_normalized
            ):

                return {
                    "category_key": key,
                    **mapping
                }


        # fallback:
        # Produkt-ID ist eindeutig gemappt,
        # auch wenn Schreibweise der Kategorie abweicht.

        for key, mapping in data.get(
            "categories",
            {}
        ).items():

            ids = []

            if mapping.get("product_id"):

                ids.append(
                    mapping.get("product_id")
                )

            ids.extend(
                mapping.get(
                    "product_ids",
                    []
                )
                or []
            )


            if product_id in ids:

                return {
                    "category_key": key,
                    **mapping
                }


        return {}


    def partner_geo_rule(
        self,
        partner
    ):

        rules = self.load_json(
            self.geo_rules_file
        )

        return (
            rules
            .get("rules", {})
            .get("partner_rules", {})
            .get(
                self.normalize(partner),
                {}
            )
        )


    def match(
        self,
        location,
        product_id
    ):

        product = self.find_product(
            product_id
        )


        if not product:

            return {
                "status": "NO_MATCH",
                "product_id": product_id,
                "reason": "product_not_found"
            }


        partner = self.normalize(
            product.get("partner")
        )

        category = self.clean(
            product.get("category")
        )


        mapping = self.find_category_mapping(
            product_id,
            category
        )


        partner_rule = self.partner_geo_rule(
            partner
        )


        product_match = bool(
            product
            and mapping
        )


        category_match = bool(
            mapping.get(
                "category_key"
            )
        )


        silo = self.clean(
            mapping.get("silo")
        )


        partner_compliant = bool(
            partner_rule.get(
                "geo_pages",
                False
            )
        )


        location_validation = (
            location.get(
                "validation",
                {}
            )
            or {}
        )


        real_location = bool(
            location_validation.get(
                "real_location"
            )
        )


        source_verified = bool(
            location_validation.get(
                "source_verified"
            )
        )


        wikidata_verified = bool(
            location_validation.get(
                "wikidata_verified"
            )
        )


        #
        # Search Intent:
        # ein bestätigtes Produkt-Kategorie-Mapping
        # plus partnerseitig erlaubte GEO-Nutzung.
        #
        search_intent_match = bool(
            product_match
            and category_match
            and partner_compliant
        )


        #
        # NICHT automatisch freigeben:
        #
        # Für CHECK24 werden echte lokale Marktdaten verlangt.
        # Für Tarifcheck echte lokale Relevanz.
        # Diese Felder müssen aus einer späteren,
        # verifizierten lokalen Datenquelle kommen.
        #
        local_data_available = bool(
            location_validation.get(
                "local_data_available",
                False
            )
        )


        unique_content = bool(
            location_validation.get(
                "unique_content",
                False
            )
        )


        geo_page_allowed = all(
            [
                real_location,
                source_verified,
                wikidata_verified,
                product_match,
                category_match,
                search_intent_match,
                partner_compliant,
                local_data_available,
                unique_content
            ]
        )


        return {

            "status":
                "MATCHED",

            "product_id":
                product_id,

            "product_name":
                self.clean(
                    product.get("name")
                ),

            "partner":
                partner,

            "category":
                self.clean(
                    mapping.get(
                        "category_key"
                    )
                    or category
                ),

            "silo":
                silo,

            "location_id":
                self.clean(
                    location.get(
                        "location_id"
                    )
                ),

            "location_name":
                self.clean(
                    location.get(
                        "name"
                    )
                ),

            "product_match":
                product_match,

            "category_match":
                category_match,

            "search_intent_match":
                search_intent_match,

            "partner_compliant":
                partner_compliant,

            "real_location":
                real_location,

            "source_verified":
                source_verified,

            "wikidata_verified":
                wikidata_verified,

            "local_data_available":
                local_data_available,

            "unique_content":
                unique_content,

            "geo_page_allowed":
                geo_page_allowed,

            "robots":
                (
                    "index, follow"
                    if geo_page_allowed
                    else "noindex, follow"
                ),

            "geo_url":
                (
                    f"https://freebasics.online/"
                    f"{silo}/"
                    f"{self.normalize(mapping.get('category_key') or category)}/"
                    f"{self.normalize(location.get('name'))}/"
                )

        }


if __name__ == "__main__":

    registry_path = Path(
        "data_master/geo_layer/geo_registry.json"
    )

    with open(
        registry_path,
        encoding="utf-8"
    ) as f:

        registry = json.load(f)


    locations = registry.get(
        "locations",
        []
    )


    if not locations:

        print(
            "NO VERIFIED LOCATIONS"
        )

    else:

        matcher = GeoProductMatcher()

        result = matcher.match(
            locations[0],
            "CHK24_001"
        )

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )
