from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json


class SearchConsoleClient:


    def __init__(
        self,
        site_url=None
    ):

        self.site_url = (
            site_url
            or "sc-domain:freebasics.online"
        )



    def _get_service(self):

        client = secretmanager.SecretManagerServiceClient()


        secret = client.access_secret_version(
            request={
                "name":
                "projects/smartcontent2050/secrets/GOOGLE_APPLICATION_CREDENTIALS_JSON/versions/latest"
            }
        ).payload.data.decode()


        info = json.loads(
            secret
        )


        credentials = (
            service_account
            .Credentials
            .from_service_account_info(
                info,
                scopes=[
                    "https://www.googleapis.com/auth/webmasters.readonly"
                ]
            )
        )


        return build(
            "searchconsole",
            "v1",
            credentials=credentials
        )



    def query_search_data(
        self,
        start_date,
        end_date
    ):

        service = self._get_service()


        request = {

            "startDate":
                start_date,

            "endDate":
                end_date,

            "dimensions":
                [
                    "query"
                ],

            "rowLimit":
                100

        }


        response = service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()


        rows = []


        for row in response.get(
            "rows",
            []
        ):

            rows.append({

                "query":
                    row["keys"][0],

                "clicks":
                    row.get(
                        "clicks",
                        0
                    ),

                "impressions":
                    row.get(
                        "impressions",
                        0
                    ),

                "ctr":
                    row.get(
                        "ctr",
                        0
                    ),

                "position":
                    row.get(
                        "position",
                        0
                    )

            })


        return {

            "site_url":
                self.site_url,

            "start_date":
                start_date,

            "end_date":
                end_date,

            "status":
                "LIVE",

            "rows":
                rows

        }



if __name__ == "__main__":


    client = SearchConsoleClient(
        "sc-domain:freebasics.online"
    )


    print(
        client.query_search_data(
            "2026-08-01",
            "2026-08-01"
        )
    )
