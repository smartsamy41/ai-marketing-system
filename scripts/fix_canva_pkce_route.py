from pathlib import Path
import shutil
from datetime import datetime

file = Path("app/main.py")

backup = Path(
    f"backups/app_main_before_canva_pkce_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
)

backup.parent.mkdir(exist_ok=True)
shutil.copy(file, backup)

print("BACKUP:", backup)

text = file.read_text()

old = """    authorization_url, state = create_canva_authorization_url(
        redirect_uri
    )

    return {
        "status": "CANVA_OAUTH_START",
        "authorization_url": authorization_url,
        "state": state
    }"""

new = """    authorization_url, state, code_verifier = create_canva_authorization_url(
        redirect_uri
    )

    return {
        "status": "CANVA_OAUTH_START",
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier
    }"""

if old not in text:
    raise Exception("CANVA OLD BLOCK NOT FOUND - STOP")

text = text.replace(old, new, 1)

file.write_text(text)

print("CANVA PKCE ROUTE UPDATE DONE")
