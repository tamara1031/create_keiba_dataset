import time

from .connection import Connection

class RawRaceDao(object):
    def __init__(self, conn:Connection):
        self.conn = conn

    def select_not_scraped_with_limit(self, limit):
        query = "select * from raw_races where scraped_at is null limit %s"
        return self.conn.execute(query, limit)

    def insert(self, netkeiba_race_id):
        query = "insert into raw_races values (null," + "%s,"*2 +"%s)"
        params = [netkeiba_race_id, None, time.time()*1000]
        return self.conn.execute(query, *params)

    def update_scraped_at(self, race_id):
        query = "update raw_races set scraped_at=%s WHERE id=%s"
        params = [time.time()*1000, race_id]
        return self.conn.execute(query, *params)