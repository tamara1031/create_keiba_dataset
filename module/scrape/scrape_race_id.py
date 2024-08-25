from module import RequestWrapper
from bs4 import BeautifulSoup
import re
import urllib.parse

# レース日程をカレンダーから取り出す
def scrape_race_date(requestWrapper: RequestWrapper, year, month):
    # リクエスト
    url = f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
    html = requestWrapper.get(url)
    html.encoding = "EUC-JP"
    soup = BeautifulSoup(html.text, "html.parser")

    table = soup.find("table", attrs={"class":"Calendar_Table"})
    a_tags = table.findAll("a")

    hrefs = [a_tag.get("href") for a_tag in a_tags]

    return [urllib.parse.parse_qs(urllib.parse.urlparse(href).query)["kaisai_date"][0] for href in hrefs]



# レース日程からレースIDを取り出す
def scrape_race_ids(requestWrapper: RequestWrapper, race_date):
     # レース日程からレースIDを抽出
    url = f"https://db.netkeiba.com/race/list/{race_date}"
    html = requestWrapper.get(url)
    html.encoding = "EUC-JP"
    soup = BeautifulSoup(html.text, "html.parser")

    race_id_set = set()
    for block in soup.findAll("dl", attrs = {"class": "race_top_hold_list"}):
        a_tags = block.findAll("a")
        hrefs = [a_tag.get("href") for a_tag in a_tags]
        race_ids = [re.findall(r"\d+", href)[0] for href in hrefs]

        race_id_set |= set(race_ids)

    return race_id_set

# カレンダーの期間内に含まれるすべてのレースIDを取り出す
def scrape_all_race_ids_from_calendar(requestWrapper: RequestWrapper, year, month):
    race_dates = scrape_race_date(requestWrapper, year, month)

    race_id_set = set()
    for race_date in race_dates:
        race_id_set |= scrape_race_ids(requestWrapper, race_date)

    return race_id_set
    

    