from module import RequestWrapper

import pandas as pd
import io
from bs4 import BeautifulSoup
import re

# レース情報を抽出する
def extract_race_info_from_soup(soup):
    all_info = soup.find("div", attrs={"class": "data_intro"})
    race_data = all_info.find("dl", attrs={"class": "racedata fc"})

    # レース番号の取得
    race_number = race_data.find("dt").get_text().replace("\n", "").replace(" ", "")

    # レースのコンディションを取得
    race_condition1 = race_data.find("dd").find("p").find("span").get_text()
    parsed_race_condition1 = race_condition1.split(u'\xa0/\xa0')

    # レースのコンディションを取得(小さいテキスト)
    race_condition2 = all_info.find("p", attrs={"class":"smalltxt"}).get_text()
    parsed_race_condition2 = race_condition2.split()

    columns = ["race_number", "race_condition", "weather", "track_condition", "starting_time", "race_date", "event_name", "race_class", "race_type"]
    merged =  [race_number] + parsed_race_condition1 + parsed_race_condition2
    return pd.DataFrame(merged, index=columns)

# 結果テーブルを抽出する
def extract_result_table_from_soup(soup):
    # tableタグを抜き出す
    table = soup.find("table", attrs={"summary":"レース結果"})
    rows = table.findAll("tr")

    # カラム名を抽出
    column_names = [column_name.get_text().replace("\n", "") for column_name in rows[0].findAll("th")]

    # 行毎にパースする
    parsed_rows = []
    for row in rows[1:]:
        parsed_row = []
        for cell in row.findAll("td"):
            text = cell.get_text().replace("\n", "")

            a_tag = cell.find("a")
            if(a_tag):
                text += "(" + a_tag.get("href") + ")"
            parsed_row.append(text)
        parsed_rows.append(parsed_row)

    # データフレームに埋め込む
    extracted = pd.DataFrame(parsed_rows, columns = column_names)
    return extracted

# 払い戻しテーブルを抽出する
def extract_payout_table_from_soup(soup):
    # tableタグを抜き出す
    tables = soup.findAll("table", attrs={"class":"pay_table_01","summary":"払い戻し"})

    index_names = []
    parsed_rows = []
    for table in tables:
        for row in table.findAll("tr"):
            index_names += [th.get_text() for th in row.findAll("th")]

            parsed_row = []
            for cell in row.findAll("td"):
                for br in cell.findAll("br"):
                    br.replace_with(";")
                text = cell.get_text()
                parsed_row.append(text)
            parsed_rows.append(parsed_row)

    # データフレームに埋め込む
    extracted = pd.DataFrame(parsed_rows, index = index_names)

    return extracted

# レースIDからレース結果を取り出す
def scrape_race_result(requestWrapper: RequestWrapper, race_id: int):
    # リクエスト
    url = f"https://db.netkeiba.com/race/{race_id}"
    html = requestWrapper.get(url)
    html.encoding = "EUC-JP"
    soup = BeautifulSoup(html.text, "html.parser")

    # レース情報の抽出
    extracted_race_info = extract_race_info_from_soup(soup)

    # 結果テーブルの抽出
    extracted_result_table = extract_result_table_from_soup(soup)

    # 払い戻しテーブルの抽出
    extracted_payout_table = extract_payout_table_from_soup(soup)

    return extracted_race_info, extracted_result_table, extracted_payout_table