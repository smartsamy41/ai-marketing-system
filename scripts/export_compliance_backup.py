import os
import json
from datetime import datetime

import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from engine.google_sheets_live import GoogleSheetsLive


OUTPUT = "audits/compliance_backup_before_fix.json"


sheets = GoogleSheetsLive(
    spreadsheet_id=os.environ["GOOGLE_SHEET_ID"],
    credentials_json=os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
)


backup = {
    "created": datetime.utcnow().isoformat(),
    "tabs": {}
}


for tab in [
    "products",
    "landingpages"
]:

    rows = sheets.read_records(
        tab,
        "A:ZZ"
    )

    backup["tabs"][tab] = rows


os.makedirs(
    "audits",
    exist_ok=True
)


with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        backup,
        f,
        indent=2,
        ensure_ascii=False
    )


print("BACKUP COMPLETE")
print("FILE:", OUTPUT)
