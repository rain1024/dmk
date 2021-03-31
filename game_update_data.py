import json
from os import listdir
from bs4 import BeautifulSoup

import requests


def get_link(name):
    cache_file = f"cache/{name}"
    if name in listdir("cache"):
        with open(cache_file) as f:
            content = f.read()
        return content
    link = f"https://dmk.fandom.com/wiki/{name}"
    r = requests.get(link)
    content = r.text
    with open(cache_file, "w") as f:
        f.write(content)
    return content


def parse_content(content):
    soup = BeautifulSoup(content, "html.parser")
    table = soup.select_one(".article-table")
    rows = table.select("tr")[1:]

    def parse_row(row):
        try:
            items = row.select("td")
            # parse character
            level = int(items[0].select_one("i").text.split()[1])
            character = items[0].select_one("a").get("title")
            characters = [{"character": character, "level": level}]
            return {"characters": characters}
            # parse activity
        except IndexError:
            return None
        except AttributeError:
            return None

    data = [parse_row(row) for row in rows]
    data = [item for item in data if item]
    return data


if __name__ == '__main__':
    name = "Minnie_Bow_Token"
    content = get_link(name)
    data = parse_content(content)
    data_file = f"data/{name}.json"
    with open(data_file, 'w') as f:
        f.write(json.dumps(data))
