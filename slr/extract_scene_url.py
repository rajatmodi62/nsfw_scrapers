import ast
import collections
import json
import re
import sys
import time
from imaplib import Commands

from playwright.sync_api import sync_playwright

# This folder will store your login session, cookies, and keys
USER_DATA_DIR = "./slr_session_data"


def setup_login():
    """Mode 1: Opens a real browser for you to log in manually."""
    print("🔓 Launching Browser for Setup...")
    print("👉 Please LOG IN to SexLikeReal in the window that opens.")
    print(
        "👉 Once you are logged in and see your homepage, simply CLOSE the browser window."
    )

    with sync_playwright() as p:
        # We use a persistent context so it saves everything to USER_DATA_DIR
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # Visible so you can interact
            viewport={"width": 1280, "height": 720},
        )

        page = browser.new_page()
        page.goto("https://www.sexlikereal.com/login")

        # Keep script running until you close the browser
        try:
            page.wait_for_timeout(9999999)
        except:
            print("✅ Setup complete! Session saved to folder.")


import json
import time

from playwright.sync_api import sync_playwright

# Must match the folder where you did the 'setup' login
USER_DATA_DIR = "./slr_session_data"


def batch_scrape_urls(url_list):
    results = {}

    with sync_playwright() as p:
        print("🚀 Launching Browser (Headless)...")

        # 1. Launch Browser ONCE
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = browser.new_page()

        # 2. Iterate through your list of links
        for url in url_list:
            print(f"➡️ Visiting: {url} ...", end="", flush=True)

            captured_json = None

            # 3. Set the Trap
            def handle_response(response):
                nonlocal captured_json
                # We look for the 'files' API call that contains the video data
                if "files" in response.url and response.status == 200:
                    try:
                        captured_json = response.json()
                    except:
                        pass

            # Attach listener
            page.on("response", handle_response)

            try:
                page.goto(url)

                # 4. Smart Wait (Max 5 seconds per link)
                start_time = time.time()
                while time.time() - start_time < 5:
                    if captured_json:
                        break
                    page.wait_for_timeout(100)

                if captured_json:
                    results[url] = dict(captured_json)
                    print(dict(captured_json))
                    print(" ✅ Captured!")
                else:
                    results[url] = {"error": "Timeout - API call not found"}
                    print(" ❌ Failed (Timeout)")

            except Exception as e:
                print(f" ❌ Error: {e}")
                results[url] = {"error": str(e)}

            # Clean up: Remove listener so they don't stack up
            page.remove_listener("response", handle_response)

            # Tiny pause to be polite to the server
            page.wait_for_timeout(2000)

        browser.close()

    return results


# --- COMMAND LINE INTERFACE ---
if __name__ == "__main__":
    # setup_login()

    # scene_urls = [
    #     "https://www.sexlikereal.com/scenes/getting-my-face-covered-by-perverted-schoolgirls-vol-2-24472",
    #     # "https://www.sexlikereal.com/scenes/gorgeous-babe-in-your-bed-76781",
    # ]
    result = batch_scrape_urls(scene_urls)

    for k, v in result.items():
        #     data = dict(v)
        max_resolution = -1
        resolution_to_link = collections.defaultdict(list)
        encodings = v["data"]["encodings"]
        for encoding in encodings:
            name = encoding["name"]
            videosources = encoding["videoSources"]

            for source in videosources:
                resolution = source["resolution"]
                link = source["url"]
                size = source["size"]
                resolution_to_link[resolution].append((size, link))
                max_resolution = max(max_resolution, resolution)
        urls = resolution_to_link[max_resolution]
        # sort by lowest size
        urls = sorted(urls, key=lambda x: x[0])
        url = urls[0][1]
        print(url)
