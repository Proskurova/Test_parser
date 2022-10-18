from bs4 import BeautifulSoup
import requests
import json

URL = ["/131067/", "/133702/", "/64106/", "/64070/", "/136241/", "/256331/", "/539467/", "/120882/", "/64071/",
       "/151877/", "/64072/", "/64068/", "/64067/", "/408658/", "/64069/", "/278351/", "/146332/", "/354764/",
       "/398172/", "/454325/", "/311526/", "/431729/", "/507705/", "/614211/", "/552624/"]
FILENAME = 'out1.json'


def get_soup(href):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    url = "https://som1.ru/shops" + href
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html5lib")
    else:
        soup = None
    return soup


def creating_data(urls):
    data = []
    for page in urls:
        soup = get_soup(page)
        if soup is None:
            break

        name = soup.find("h1").text
        classes = soup.find_all("table", class_="shop-info-table")
        for cl in classes:
            td = cl.find_all("td")
            address = td[2].text
            phones = td[5].text.split(",")
            working_hours = td[8].text.split(",")

            item = {
                "address": address,
                "name": name,
                "phones": phones,
                "working_hours": working_hours,

            }
            data.append(item)
    return data


def main():
    data = creating_data(URL)
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()