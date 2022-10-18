from bs4 import BeautifulSoup
import requests
import json

URL = "https://oriencoop.cl/sucursales.htm"
FILENAME = 'out.json'


def get_soup(href):
    response = requests.get(href)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        soup = None
    return soup


def create_page(url):
    list_page = []
    url_all = get_soup(url).find_all("ul", class_="sub-menu")
    for ul in url_all:
        a = ul.find_all("a")
        for pages in a:
            page = pages.get("href")[-3:].replace('/', '')
            list_page.append(page)
    return list_page


def creating_data(urls):
    data = []
    for page in create_page(urls):
        url_page = "https://oriencoop.cl/sucursales/{}".format(page)
        soup = get_soup(url_page)
        if soup is None:
            break

        classes = soup.find_all("div", class_="sucursal")
        for cl in classes:
            span = cl.find_all("span")
            address = span[0].text
            latlon = [float(i[2:]) for i in cl.find("iframe")["src"].split("!") if i[:2] == "2d" or i[:2] == "3d"]
            name = cl.find("h3").text
            phones = [span[1].text]
            working_hours = [span[i].text for i in range(len(span)) if len(span[i].contents) >= 2]

            item = {
                "address": address,
                "latlon": latlon,
                "name": name,
                "phones": phones,
                "working_hours": working_hours,

            }
            data.append(item)
    return data


def main():
    data = creating_data(URL)

    with open(FILENAME, "w", encoding="utf-32") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()