from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import threading
import itertools
import sys
import random


##########The Spinner.
class Spinner:
    def __init__(self, message="Working"):
        self.message = message
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        for frame in itertools.cycle(".*oO080Oo*."):
            if self._stop.is_set():
                break
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        # Erase the spinner line
        sys.stdout.write("\r" + " " * (len(self.message) + 3) + "\r")
        sys.stdout.flush()

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *args):
        self._stop.set()
        self._thread.join()
##########The Spinner end.

#The seed url and the initial states.
url = "https://en.wikipedia.org/wiki/Existence"
url_looking_for = "https://en.wikipedia.org/wiki/God"
looking_for = "God"
counter = 1
found = False

# Clear the screen at the start.
print("\033[2J\033[3J\033[H", end="")

while not found:
    try:
        with Spinner("Seeking..."):
            req = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                }
            )

            with urlopen(req, timeout=10) as fp:
                soup = BeautifulSoup(fp, "html.parser")

        title = soup.find("h1").get_text(strip=True)

        #Print and save the output.
        print(f"\n{counter}. visited {title} at {url}\n")
        with open("output/history.md", "a") as file:
            file.write(f"{counter}. visited [{title}]({url})\n\n")
        with open("output/poem.txt", "a") as file:
            file.write(f"step N°{counter}: {title}. ")

        

        if title == looking_for:
            with open("output/history.md", "a") as file:
                file.write(f"Found {looking_for} after visiting {counter} pages.\n")
            with open("output/poem.txt", "a") as file:
                file.write(f"found God.")
            print(f"Found {looking_for} after visiting {counter} pages!\n")
            found = True

        else:
            # Get all the links
            all_links = soup.find_all("a", href=True)
            links = [link["href"] for link in all_links]

            # Get clean Wikipedia links
            wiki_url = "https://en.wikipedia.org/wiki/"
            clean_links = []

            for link in links:
                if (
                    wiki_url in link
                    and "#" not in link
                    and "File" not in link
                    and "Help" not in link
                    and "Template" not in link
                    and "Talk" not in link
                    and "Wikipedia" not in link
                    and "Category" not in link
                    and "ISO" not in link
                    and "Special" not in link
                    and "ISBN" not in link
                ):
                    clean_links.append(link)

            # Shuffle the links
            random.shuffle(clean_links)

            if (url_looking_for in clean_links):
                url = url_looking_for

            else:
                # Try links until one works
                next_url = None

                for link in clean_links:
                    try:
                        req = Request(
                            link,
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                            }
                        )

                        with urlopen(req, timeout=10):
                            next_url = link
                            break

                    except Exception as e:
                        print(f'skipping {next_url}')

                if next_url:
                    url = next_url
                else:
                    print("No working links found on this page.")
                    break
        counter += 1

    except Exception as e:
        print(f"Error accessing {url}: {e}")
        break

