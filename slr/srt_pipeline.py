import json
from pathlib import Path

import requests

# File to store your persistent login state
COOKIE_STORAGE = Path("slr_session.json")


def get_persistent_session():
    session = requests.Session()

    if COOKIE_STORAGE.exists():
        # Load the "memory" of your last login
        with open(COOKIE_STORAGE, "r") as f:
            session.cookies.update(json.load(f))
        print("✅ Session restored from persistent storage.")
    else:
        # PASTE THE VALUES FROM YOUR IMAGES HERE ONCE
        initial_cookies = {
            "refresh_jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3Njk3OTk3OTguMjgxMzI2LCJuYmYiOjE3Njk3OTk3OTguMjgxMzI2LCJleHAiOjE3NzIzOTE3OTguMjgxMzI2LCJzdWIiOiI1ZTE5YzNiMDk3MzZmZTc2ZGMzNTEzMDYiLCJ0b2tlblR5cGUiOiJyZWZyZXNoIiwicHJvamVjdCI6MSwiY2xpZW50VHlwZSI6IndlYiIsInNvdXJjZSI6MSwiaXAiOiI1Mi4xMjQuNDUuMTciLCJyb2xlcyI6WzFdLCJqdGkiOiI2OTdkMDA3NjMyMzUwZjlhYTMwNGMwYmQifQ.uAClgRO8JiZUt-AkTPr5RUMWXQB_8LHhu9wBWNIxldg",
            "session": "PASTE_VALUE_FROM_IMAGE",
            "cf_clearance": "SqAkCA2MJCpbFs_jNsL3K8gbvwhr7iKDRXfry_6ZKHM-1767839383-1.2.1.1-P0wYB_bxe1rABN.1FRBkttCOf0T0Z6IzrJOZ6DhjLHz9KEioYti1NA_zn_thetAliXynn7m6jHAZvyuTeq7eYQ258Ujg8EQ9SFjVVslM2Ws7_6c8Ga_S_WFKgxfIbMGz5gLcJOlNFzzGryXWkgHElAugZmJ4n_NT2mXxJQQrEmqzHknKSBnTxYw5D3c9XsMci2IgPr3FSnljI_M7HgHJgFN9wf9SKFNKmABV5rM56jw",
        }
        session.cookies.update(initial_cookies)
        # Save them so you don't have to do this again
        with open(COOKIE_STORAGE, "w") as f:
            json.dump(session.cookies.get_dict(), f)
        print("💾 Initial persistent session saved.")

    # These headers make your script look like a real browser
    session.headers.update(
        {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...",
            "client-type": "web",
            "project": "1",
        }
    )
    return session


# Usage
s = get_persistent_session()
# This request now "inherits" your browser's persistent identity
response = s.get("https://api.sexlikereal.com/v3/scenes/24472/files")
print(response.json())
