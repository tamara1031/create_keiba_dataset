from tqdm import tqdm
import re

from module import RequestWrapper, RawRaceDao, Connection
from module import RawRaceInformationDao, RawRaceResultDao, RawRacePayoutDao
from module import scrape_race_result

# scrape時に便宜上結合してしまったデータを分離する
def extract_name_and_netkeiba_id_from_value(value: str):
    groups = re.search(r'^(?P<name>.+)\((?P<href>.+)\)$', value)
    
    return groups.group("name"), groups.group("href")

# インスタンスの生成
requestWrapper = RequestWrapper(request_interval_milli=1500)
conn = Connection(config_key="raw_data")
raceDao = RawRaceDao(conn)
infoDao = RawRaceInformationDao(conn)
resultDao = RawRaceResultDao(conn)
payoutDao = RawRacePayoutDao(conn)

races = raceDao.select_not_scraped_with_limit(10000)
for race in tqdm(races):
    race_id = race["id"]

    netkeiba_race_id = race["netkeiba_race_id"]
    
    info, result_table, payout_table = scrape_race_result(requestWrapper, netkeiba_race_id)

    # レース情報をinsert
    info = info[0]
    infoDao.insert(
        race_id, 
        info["race_number"], 
        info["race_condition"], 
        info["weather"], 
        info["track_condition"], 
        info["starting_time"],
        info["race_date"],
        info["event_name"],
        info["race_class"],
        info["race_type"],
    )

    # レース結果のinsert
    for i, result in result_table.iterrows():
        horse_name, horse_href = extract_name_and_netkeiba_id_from_value(result["馬名"])
        jockey_name, jockey_href = extract_name_and_netkeiba_id_from_value(result["騎手"])
        trainer_name, trainer_href = extract_name_and_netkeiba_id_from_value(result["調教師"])
        owner_name, owner_href = extract_name_and_netkeiba_id_from_value(result["馬主"])
        horse_id = horse_href.split("/")[-2]
        jockey_id = jockey_href.split("/")[-2]
        trainer_id = trainer_href.split("/")[-2]
        owner_id = owner_href.split("/")[-2]

        resultDao.insert(
            race_id, 
            result["着順"], 
            result["枠番"], 
            result["馬番"], 
            horse_name,
            horse_id,
            result["性齢"], 
            result["斤量"],
            jockey_name,
            jockey_id,
            result["タイム"],
            result["着差"],
            result["通過"],
            result["上り"],
            result["単勝"],
            result["人気"],
            result["馬体重"],
            trainer_name,
            trainer_id,
            owner_name,
            owner_id,
            result["賞金(万円)"]
        )

    # payoutテーブルinsert
    for i, payout in payout_table.iterrows():
        payoutDao.insert(
            race_id,
            payout.name,
            payout[0],
            payout[1],
            payout[2]
        )

    # 処理済フラグを立てる
    raceDao.update_scraped_at(race_id)
    conn.commit()
