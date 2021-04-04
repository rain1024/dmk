import json
from os import listdir
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


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


def update_character(name):
    name_norm = name.replace(" ", "_")
    link = f"https://dmk.fandom.com/wiki/{name_norm}"
    r = requests.get(link)
    content = r.text
    soup = BeautifulSoup(content, "html.parser")
    level_table = soup.select_one(".article-table")

    links = level_table.select("tr")[1].select("td a")[:3]
    def extract_level_requirements(level_table):
        rows = level_table.select("tr")[1:11]
        def extract_row(i, row):
            output = [_.text.strip() for _ in row.select("td")]
            output = output[1:-1]
            output = [name, i+1] + output
            return output
        output = [extract_row(i, _) for i, _ in enumerate(rows)]
        return output
    level_requirements = extract_level_requirements(level_table)
    items = [link.attrs['title'] for link in links]
    hrefs = [link.attrs['href'] for link in links]

    def parse_item_page(href):
        link = f"https://dmk.fandom.com{href}"
        r = requests.get(link)
        content = r.text
        soup = BeautifulSoup(content, "html.parser")
        obtain_rows = soup.select("table.article-table tr")[1:]
        for row in obtain_rows:
            table_data = row.select("td")
            print(0)
            try:
                if row.select("th")[0].text.split() == "Other Source":
                    break
            except IndexError:
                pass
        rarity = soup.find(attrs={"data-source": "rarity"}).select_one(".pi-font a").text
        output = {
            "rarity": rarity
        }
        return output

    items_rarity = [parse_item_page(href)["rarity"] for href in hrefs]

    rows = [(name, item, rarity, f"Token {i + 1}") for i, (item, rarity) in enumerate(zip(items, items_rarity))]
    n_cols = 30
    n_rows = 30
    df = pd.DataFrame(data=np.empty((n_rows, n_cols), dtype=str), columns=range(n_cols))
    df.iloc[1:4, :4] = rows
    df.iloc[1:11, 6:6+7] = level_requirements
    df.to_csv(f"data/{name_norm}.csv", index=False, header=False, sep=";")
    print(name)


if __name__ == '__main__':
    # name = "Minnie_Bow_Token"
    # content = get_link(name)
    # data = parse_content(content)
    # data_file = f"data/{name}.json"
    # with open(data_file, 'w') as f:
    #     f.write(json.dumps(data))
    name = 'Mike Wazowski'
    update_character(name)
