import json
import requests

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone


FREEBASICS_DOMAIN = "freebasics.online"

REGISTRY_FILE = Path(
    "data_master/authority_layer/backlink_registry.json"
)


class LinkParser(HTMLParser):

    def __init__(self):

        super().__init__()

        self.links = []


    def handle_starttag(
        self,
        tag,
        attrs
    ):

        if tag.lower() != "a":
            return

        data = dict(attrs)

        href = data.get(
            "href",
            ""
        )

        rel = data.get(
            "rel",
            ""
        )

        if isinstance(rel, list):
            rel = " ".join(rel)

        self.links.append(
            {
                "href": href,
                "rel": rel,
                "anchor": ""
            }
        )


    def handle_data(
        self,
        data
    ):

        if not self.links:
            return

        text = str(
            data or ""
        ).strip()

        if not text:
            return

        current = self.links[-1]

        if current.get("anchor"):
            current["anchor"] += " " + text
        else:
            current["anchor"] = text


class BacklinkAnalyzer:

    def __init__(self):

        self.registry_file = REGISTRY_FILE

        self.headers = {
            "User-Agent":
                "FreeBasicsBacklinkMonitor/1.0 "
                "(https://freebasics.online)"
        }


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(
        value
    ):

        if value is None:
            return ""

        return str(value).strip()


    @staticmethod
    def normalize_domain(
        domain
    ):

        domain = str(
            domain or ""
        ).lower().strip()

        if domain.startswith(
            "www."
        ):

            domain = domain[4:]

        return domain


    @classmethod
    def normalize_freebasics_url(
        cls,
        url
    ):

        try:

            parsed = urlparse(
                url
            )

            domain = cls.normalize_domain(
                parsed.netloc
            )

            if (
                domain == FREEBASICS_DOMAIN
                or domain.endswith(
                    "." + FREEBASICS_DOMAIN
                )
            ):

                path = parsed.path or ""

                if path == "/":
                    path = ""

                query = (
                    "?" + parsed.query
                    if parsed.query
                    else ""
                )

                fragment = (
                    "#" + parsed.fragment
                    if parsed.fragment
                    else ""
                )

                return (
                    "https://"
                    + domain
                    + path
                    + query
                    + fragment
                )

        except Exception:
            pass

        return url


    @classmethod
    def is_freebasics_url(
        cls,
        url
    ):

        try:

            parsed = urlparse(
                url
            )

            domain = cls.normalize_domain(
                parsed.netloc
            )

            return (
                domain == FREEBASICS_DOMAIN
                or domain.endswith(
                    "." + FREEBASICS_DOMAIN
                )
            )

        except Exception:

            return False


    @staticmethod
    def load_json(
        path
    ):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    @staticmethod
    def save_json(
        path,
        data
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


    # =========================================================
    # URL ANALYSIS
    # =========================================================

    def analyze_url(
        self,
        url
    ):

        parsed = urlparse(
            url
        )

        return {

            "url":
                url,

            "domain":
                self.normalize_domain(
                    parsed.netloc
                ),

            "scheme":
                parsed.scheme,

            "path":
                parsed.path,

            "status":
                "ready_for_analysis"

        }


    # =========================================================
    # FETCH SOURCE PAGE
    # =========================================================

    def fetch_page(
        self,
        source_url
    ):

        try:

            response = requests.get(
                source_url,
                headers=self.headers,
                timeout=20,
                allow_redirects=True
            )

            return {

                "status":
                    "OK",

                "http_status":
                    response.status_code,

                "final_url":
                    response.url,

                "content_type":
                    response.headers.get(
                        "Content-Type",
                        ""
                    ),

                "html":
                    response.text
                    if response.ok
                    else ""

            }

        except Exception as error:

            return {

                "status":
                    "ERROR",

                "http_status":
                    None,

                "final_url":
                    source_url,

                "content_type":
                    "",

                "html":
                    "",

                "error":
                    str(error)

            }


    # =========================================================
    # LINK EXTRACTION
    # =========================================================

    def extract_links(
        self,
        html,
        base_url
    ):

        parser = LinkParser()

        try:

            parser.feed(
                html
            )

        except Exception:

            return []

        links = []

        for item in parser.links:

            href = self.clean(
                item.get(
                    "href"
                )
            )

            if not href:
                continue

            absolute = urljoin(
                base_url,
                href
            )

            links.append(
                {

                    "url":
                        absolute,

                    "anchor":
                        self.clean(
                            item.get(
                                "anchor"
                            )
                        ),

                    "rel":
                        self.clean(
                            item.get(
                                "rel"
                            )
                        )

                }
            )

        return links


    # =========================================================
    # FIND FREE BASICS BACKLINKS
    # =========================================================

    def find_freebasics_links(
        self,
        source_url
    ):

        page = self.fetch_page(
            source_url
        )

        if page.get(
            "status"
        ) != "OK":

            return {

                "status":
                    "ERROR",

                "source_url":
                    source_url,

                "http_status":
                    page.get(
                        "http_status"
                    ),

                "error":
                    page.get(
                        "error",
                        ""
                    ),

                "links":
                    []

            }


        links = self.extract_links(
            page.get(
                "html",
                ""
            ),
            page.get(
                "final_url",
                source_url
            )
        )


        matches = [

            item

            for item in links

            if self.is_freebasics_url(
                item.get(
                    "url"
                )
            )

        ]


        return {

            "status":
                (
                    "FOUND"
                    if matches
                    else "NOT_FOUND"
                ),

            "source_url":
                source_url,

            "final_source_url":
                page.get(
                    "final_url"
                ),

            "http_status":
                page.get(
                    "http_status"
                ),

            "content_type":
                page.get(
                    "content_type"
                ),

            "links":
                matches

        }


    # =========================================================
    # REL CLASSIFICATION
    # =========================================================

    @staticmethod
    def classify_rel(
        rel
    ):

        values = {
            x.strip().lower()
            for x in str(
                rel or ""
            ).split()
            if x.strip()
        }

        return {

            "nofollow":
                "nofollow" in values,

            "sponsored":
                "sponsored" in values,

            "ugc":
                "ugc" in values,

            "follow":
                not any(
                    x in values
                    for x in {
                        "nofollow",
                        "sponsored",
                        "ugc"
                    }
                )

        }


    # =========================================================
    # REGISTRY
    # =========================================================

    def load_registry(
        self
    ):

        data = self.load_json(
            self.registry_file
        )

        if data:
            return data


        return {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "backlink_registry",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "real_backlinks_only":
                        True,

                    "source_page_must_be_fetchable":
                        True,

                    "freebasics_link_must_exist":
                        True,

                    "no_artificial_backlinks":
                        True,

                    "no_fabricated_metrics":
                        True

                },

            "summary":
                {

                    "total":
                        0,

                    "active":
                        0,

                    "lost":
                        0,

                    "errors":
                        0

                },

            "backlinks":
                [],

            "updated_at":
                None

        }


    def save_registry(
        self,
        registry
    ):

        backlinks = (
            registry.get(
                "backlinks",
                []
            )
            or []
        )


        active = sum(
            1
            for x in backlinks
            if x.get(
                "status"
            )
            == "ACTIVE"
        )


        lost = sum(
            1
            for x in backlinks
            if x.get(
                "status"
            )
            == "LOST"
        )


        errors = sum(
            1
            for x in backlinks
            if x.get(
                "status"
            )
            == "ERROR"
        )


        registry[
            "summary"
        ] = {

            "total":
                len(
                    backlinks
                ),

            "active":
                active,

            "lost":
                lost,

            "errors":
                errors

        }


        registry[
            "updated_at"
        ] = datetime.now(
            timezone.utc
        ).isoformat()


        self.save_json(
            self.registry_file,
            registry
        )


    # =========================================================
    # REGISTER VERIFIED SOURCE PAGE
    # =========================================================

    def register_source(
        self,
        source_url,
        source_type="external_reference"
    ):

        result = self.find_freebasics_links(
            source_url
        )


        now = datetime.now(
            timezone.utc
        ).isoformat()


        registry = self.load_registry()

        backlinks = registry.get(
            "backlinks",
            []
        )


        existing = {

            (
                x.get(
                    "source_url"
                ),
                x.get(
                    "target_url"
                )
            ):
                x

            for x in backlinks

        }


        # =====================================================
        # FETCH ERROR
        # =====================================================

        if result.get(
            "status"
        ) == "ERROR":

            return {

                "status":
                    "ERROR",

                "source_url":
                    source_url,

                "error":
                    result.get(
                        "error"
                )

            }


        # =====================================================
        # NO BACKLINK
        # =====================================================

        if result.get(
            "status"
        ) == "NOT_FOUND":

            return {

                "status":
                    "NOT_FOUND",

                "source_url":
                    source_url,

                "http_status":
                    result.get(
                        "http_status"
                ),

                "backlinks_found":
                    0

            }


        registered = []


        for link in result.get(
            "links",
            []
        ):

            target_url = (
                self.normalize_freebasics_url(
                    link.get(
                        "url"
                    )
                )
            )

            key = (
                source_url,
                target_url
            )


            rel = self.classify_rel(
                link.get(
                    "rel"
                )
            )


            record = {

                "backlink_id":
                    (
                        self.normalize_domain(
                            urlparse(
                                source_url
                            ).netloc
                        )
                        + "::"
                        + target_url
                    ),

                "source_url":
                    source_url,

                "source_domain":
                    self.normalize_domain(
                        urlparse(
                            source_url
                        ).netloc
                    ),

                "source_type":
                    source_type,

                "target_url":
                    target_url,

                "anchor_text":
                    link.get(
                        "anchor",
                        ""
                    ),

                "rel":
                    link.get(
                        "rel",
                        ""
                    ),

                "follow":
                    rel.get(
                        "follow"
                    ),

                "nofollow":
                    rel.get(
                        "nofollow"
                    ),

                "sponsored":
                    rel.get(
                        "sponsored"
                    ),

                "ugc":
                    rel.get(
                        "ugc"
                    ),

                "http_status":
                    result.get(
                        "http_status"
                    ),

                "link_verified":
                    True,

                "status":
                    "ACTIVE",

                "first_seen":
                    (
                        existing.get(
                            key,
                            {}
                        ).get(
                            "first_seen"
                        )
                        or now
                    ),

                "last_checked":
                    now

            }


            if key in existing:

                existing[
                    key
                ].update(
                    record
                )

            else:

                backlinks.append(
                    record
                )


            registered.append(
                record
            )


        registry[
            "backlinks"
        ] = backlinks


        self.save_registry(
            registry
        )


        return {

            "status":
                "REGISTERED",

            "source_url":
                source_url,

            "backlinks_found":
                len(
                    registered
                ),

            "records":
                registered

        }


    # =========================================================
    # RECHECK EXISTING REGISTRY
    # =========================================================

    def recheck_all(
        self
    ):

        registry = self.load_registry()

        backlinks = (
            registry.get(
                "backlinks",
                []
            )
            or []
        )


        source_urls = sorted(
            {
                x.get(
                    "source_url"
                )

                for x in backlinks

                if x.get(
                    "source_url"
                )
            }
        )


        results = []


        for source_url in source_urls:

            verification = (
                self.find_freebasics_links(
                    source_url
                )
            )

            results.append(
                verification
            )


            current_targets = {

                x.get(
                    "url"
                )

                for x in verification.get(
                    "links",
                    []
                )

            }


            for record in backlinks:

                if record.get(
                    "source_url"
                ) != source_url:

                    continue


                record[
                    "last_checked"
                ] = datetime.now(
                    timezone.utc
                ).isoformat()


                if verification.get(
                    "status"
                ) == "ERROR":

                    record[
                        "status"
                    ] = "ERROR"

                    continue


                if record.get(
                    "target_url"
                ) in current_targets:

                    record[
                        "status"
                    ] = "ACTIVE"

                    record[
                        "link_verified"
                    ] = True

                else:

                    record[
                        "status"
                    ] = "LOST"

                    record[
                        "link_verified"
                    ] = False


        registry[
            "backlinks"
        ] = backlinks


        self.save_registry(
            registry
        )


        return {

            "status":
                "COMPLETE",

            "sources_checked":
                len(
                    source_urls
                ),

            "backlinks":
                registry.get(
                    "summary"
                )

        }


if __name__ == "__main__":

    analyzer = BacklinkAnalyzer()

    registry = analyzer.load_registry()

    analyzer.save_registry(
        registry
    )

    print(
        "BACKLINK REGISTRY READY"
    )

    print(
        "FILE:",
        analyzer.registry_file
    )

    print(
        "TOTAL:",
        registry.get(
            "summary",
            {}
        ).get(
            "total",
            0
        )
    )
