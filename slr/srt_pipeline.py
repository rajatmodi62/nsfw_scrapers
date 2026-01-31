import re

import browser_cookie3
import requests


def get_html_with_cookies(url):
    cj = browser_cookie3.chrome()
    response = requests.get(url, cookies=cj)
    return response.text


all_urls = []

######### scrape the scene page for which one contains ai subs ###############
#### like this https://www.sexlikereal.com/tags/subtitles-ai-vr?p=200########

n_pages = 330
for done, page in enumerate(range(1, n_pages + 1)):
    print(f"Processing page {page} of {n_pages} ({done + 1}/{n_pages})")
    url = f"https://www.sexlikereal.com/tags/subtitles-ai-vr?p={page}"

    cj = browser_cookie3.chrome()
    response = requests.get(url, cookies=cj)
    data = response.text

    regex = r'https:(?:\\/\\/|//)www\.sexlikereal\.com\\?/scenes\\?/[^" ]+'

    # Find all occurrences
    raw_links = re.findall(regex, data)

    # Clean the links (replace \/ with /) and remove duplicates
    clean_links = []
    for link in raw_links:
        normalized = link.replace("\\/", "/").replace("\\", "")
        if normalized not in clean_links:
            clean_links.append(normalized)
            all_urls.append(normalized)
    print(clean_links)
    print("done ", done + 1, "/", n_pages)
####### add .srt links to all_urls#############
all_urls = list(set(all_urls))
####### download subtitle for a particular scene ##############
#### for eg, <https://cdn-vr.sexlikereal.com/subtitles/8727/en/311383_streaming.srt>####

for done, url in enumerate(all_urls):
    print(f"Processing scene {done + 1} of {len(all_urls)}")

    # url = "https://www.sexlikereal.com/scenes/legal-cast-the-movie-55537"
    data = get_html_with_cookies(url)

    ############# FIND SRT LINKS IN HTML ##############
    ######## FILTER ONLY EN ####################

    pattern = r"https?://[0-9a-zA-Z\.\-_/]+?\.srt"

    srt_links = re.findall(pattern, data)

    # # Remove duplicates by converting to a set and back to a list
    unique_links = list(set(srt_links))

    print("unique links", unique_links)
    for link in unique_links:
        if "en" in link:
            scene_id = link.split("/")[-3] + ".srt"
            response = requests.get(link)

            # Save the file with the scene ID as the filename

            with open(scene_id, "wb") as f:
                f.write(response.content)
            print(f"Downloaded subtitle: {scene_id}")
