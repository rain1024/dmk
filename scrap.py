import requests
import bs4

r = requests.get('https://disneymagickingdomswiki.fandom.com/wiki/Merlin')

a = bs4.BeautifulSoup(r.text, features="html.parser")
dom = a.select("div[class='mw-parser-output'] h2")[0]
title = str(dom.contents[0])
print(title)
print(0)

