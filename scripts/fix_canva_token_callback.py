from pathlib import Path
import shutil
from datetime import datetime

file = Path("app/main.py")

backup = Path(
    f"backups/app_main_before_canva_token_callback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
)

backup.parent.mkdir(exist_ok=True)
shutil.copy(file, backup)

print("BACKUP:", backup)

text = file.read_text()

old = '''    return {
        "status": "CANVA_CALLBACK_RECEIVED",
        "code_received": True,
        "state_received": bool(state)
    }'''

new = '''    if not state:
        raise HTTPException(
            status_code=400,
            detail="Missing Canva OAuth state"
        )

    session = CANVA_PKCE_STORE.get(state)

    if not session:
        raise HTTPException(
            status_code=400,
            detail="Unknown Canva OAuth state"
        )

    token = exchange_canva_code(
        code,
        session["redirect_uri"],
        session["code_verifier"]
    )

    return {
        "status": "CANVA_CONNECTED",
        "token_received": True,
        "token_type": token.get("token_type"),
        "expires_in": token.get("expires_in")
    }'''

if old not in text:
    raise Exception("CANVA CALLBACK BLOCK NOT FOUND - STOP")

text = text.replace(old, new, 1)

file.write_text(text)

print("CANVA TOKEN CALLBACK UPDATE DONE")
