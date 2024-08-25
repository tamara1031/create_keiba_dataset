from .connection import Connection

class RawRacePayoutDao(object):
    def __init__(self, conn:Connection):
        self.conn = conn

    def insert(self, raw_race_id, payout_type, horse_number, payout, favorite):
        query = "insert into raw_race_payouts values (null," + "%s,"*4 + "%s)"
        params = [raw_race_id, payout_type, horse_number, payout, favorite]
        return self.conn.execute(query, *params)