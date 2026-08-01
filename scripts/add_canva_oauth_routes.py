from pathlib import Path
import shutil
from datetime import datetime

file = Path("app/main.py")

backup = Path(
    f"backups/app_main_canva_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
)

backup.parent.mkdir(exist_ok=True)

shutil.copy(file, backup)

print("BACKUP:", backup)

text = file.read_text()

import_line = """
from engine.canva.canva_oauth import (
    create_canva_authorization_url,
    exchange_canva_code
)
"""

if "engine.canva.canva_oauth" not in text:
    marker = "from app.compliance_newsletter import register_doi_pending, confirm_doi_token"
    text = text.replace(
        marker,
        marker + import_line
    )
    print("IMPORT ADDED")
else:
    print("IMPORT EXISTS")


routes = '''

# ==================================================
# CANVA CONNECT API OAUTH
# ==================================================

@app.get("/canva/login")
def canva_login():

    redirect_uri = "https://freebasics.online/canva/callback"

    authorization_url, state = create_canva_authorization_url(
        redirect_uri
    )

    return {
        "status": "CANVA_OAUTH_START",
        "authorization_url": authorization_url,
        "state": state
    }


@app.get("/canva/callback")
def canva_callback(
    code: str = None,
    state: str = None
):

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing Canva authorization code"
        )

    return {
        "status": "CANVA_CALLBACK_RECEIVED",
        "code_received": True,
        "state_received": bool(state)
    }


# ==================================================
# END CANVA CONNECT API OAUTH
# ==================================================

'''

if '"/canva/login"' not in text:
    marker = '@app.post("/run")'
    text = text.replace(
        marker,
        routes + "\n" + marker
    )
    print("ROUTES ADDED")
else:
    print("ROUTES EXISTS")


file.write_text(text)

print("CANVA INTEGRATION UPDATE COMPLETE")
