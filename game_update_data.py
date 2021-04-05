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
            output = [name, i + 1] + output
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
        item_name = soup.select_one("#firstHeading").text
        obtain_rows = soup.select("table.article-table tr")[1:]
        obtain_data = []
        for row in obtain_rows:
            try:
                row.select("th")[0]
                if row.select("th")[0].text.strip() == "Other Source":
                    break
            except IndexError:
                pass
            row_data_items = row.select("td")
            time = row_data_items[3].text.strip()
            c1_name = row_data_items[0].select_one("a").attrs["title"]
            c1_level = row_data_items[0].select_one("small").text.split(" ")[1]

            try:
                extra = row_data_items[1].select_one("small a").attrs["title"]
            except AttributeError:
                extra = ""
            try:
                c2_name = row_data_items[2].select_one("a").attrs["title"]
                c2_level = row_data_items[2].select_one("small").text.split(" ")[1]
            except AttributeError:
                c2_name = ""
                c2_level = ""

            obtain_data.append({
                "item_name": item_name,
                "time": time,
                "c1": c1_name,
                "c1_level": c1_level,
                "c2": c2_name,
                "c2_level": c2_level,
                "extra": extra
            })
            # print(0)
        rarity = soup.find(attrs={"data-source": "rarity"}).select_one(".pi-font a").text
        output = {
            "rarity": rarity,
            "obtain": obtain_data
        }
        return output

    items_data = [parse_item_page(href) for href in hrefs]
    items_rarity = [item["rarity"] for item in items_data]
    items_obtain = [item["obtain"] for item in items_data]
    items_obtain = [item for sub in items_obtain for item in sub]
    items_obtain = [list(item.values()) for item in items_obtain]

    rows = [(name, item, rarity, f"Token {i + 1}") for i, (item, rarity) in enumerate(zip(items, items_rarity))]
    n_cols = 30
    n_rows = 30
    df = pd.DataFrame(data=np.empty((n_rows, n_cols), dtype=str), columns=range(n_cols))
    df.iloc[0:len(items_obtain), 0:7] = items_obtain
    df.iloc[0:3, 8:8+4] = rows
    df.iloc[0:10, 14:14+7] = level_requirements

    df.to_csv(f"data/{name_norm}.csv", index=False, header=False, sep=";")
    print(name)


if __name__ == '__main__':
    # name = "Minnie_Bow_Token"
    # content = get_link(name)
    # data = parse_content(content)
    # data_file = f"data/{name}.json"
    # with open(data_file, 'w') as f:
    #     f.write(json.dumps(data))
    name = 'Flynn'
    update_character(name)
