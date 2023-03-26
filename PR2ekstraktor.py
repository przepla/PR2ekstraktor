import requests
import re
import argparse
import os

parser = argparse.ArgumentParser(description='Download MP3 files from one or more URLs.')
parser.add_argument('urls', metavar='URL', nargs='+', help='the URL(s) to download from')
args = parser.parse_args()

for url in args.urls:
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the title of the webpage
        title_match = re.search(r'<title>\s*(.+?)\s*</title>', response.text)
        if title_match:
            # Remove any illegal characters from the title
            title = "".join(c if c.isalnum() or c.isspace() else "_" for c in title_match.group(1))
            mp3_url_match = re.search(r'//static\.prsa\.pl/.+?\.mp3', response.text)
            if mp3_url_match:
                mp3_url = "http:" + mp3_url_match.group(0)
                print("Downloading MP3 from URL:", mp3_url)
                response = requests.get(mp3_url)
                if response.status_code == 200:
                    # Save the MP3 file with the title as its name
                    with open(f"{title}.mp3", "wb") as f:
                        f.write(response.content)
                    print("MP3 downloaded successfully!")
                else:
                    print("Failed to download MP3")
            else:
                print("MP3 URL not found on the page")
        else:
            print("Title not found on the page")
    else:
        print("Failed to fetch the URL")

