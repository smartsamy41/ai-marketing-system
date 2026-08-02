from google.cloud import firestore
import time

db = firestore.Client()

COLLECTION = "canva_pkce"


def save_pkce_state(state, redirect_uri, code_verifier):

    db.collection(COLLECTION).document(state).set({
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "created_at": int(time.time())
    })


def get_pkce_state(state):

    doc = db.collection(COLLECTION).document(state).get()

    if not doc.exists:
        return None

    return doc.to_dict()


def delete_pkce_state(state):

    db.collection(COLLECTION).document(state).delete()
