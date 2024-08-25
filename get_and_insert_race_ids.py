from tqdm import tqdm

from module import RequestWrapper, RawRaceDao, Connection
from module import scrape_all_race_ids_from_calendar

requestWrapper = RequestWrapper(request_interval_milli=2000)
conn = Connection(config_key="raw_data")
dao = RawRaceDao(conn)

for year in tqdm(range(2019, 2025)):
    for month in tqdm(range(1, 13)):
        
        race_ids = scrape_all_race_ids_from_calendar(requestWrapper, year, month)

        for race_id in race_ids:
            try:
                dao.insert(race_id)
                conn.commit()
            except Exception as e:
                # insert失敗は処理を継続
                # TODO: duplicated entryだけ判定する
                print(f"{e.__class__.__name__}: {e}") 
                print(f"failed to execute query: {year}, {month}, {race_id}")

