import os

from requests.sessions import TooManyRedirects

all_ready_downloaded_urls = set()
with open("already_download_urls.txt") as f:
    for line in f:
        print(line)
        all_ready_downloaded_urls.add(line.strip())

# print(len(all_ready_downloaded_urls))
to_download_urls = set()

with open("urls.txt") as f:
    for line in f:
        # print("check new", line)
        url = line.strip()
        if url not in all_ready_downloaded_urls:
            to_download_urls.add(url)
            # print("to download", url)
        else:
            print("skipping")

# print(len(to_download_urls))
with open("to_download_urls.txt", "w") as f:
    for url in to_download_urls:
        f.write(url + "\n")
