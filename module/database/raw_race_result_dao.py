from .connection import Connection

class RawRaceResultDao(object):
    def __init__(self, conn:Connection):
        self.conn = conn

    def insert(self, raw_race_id, rank, frame_number, 
                horse_number, horse_name, netkeiba_horse_id, horse_gender_age, 
                carried_weight, jockey_name, netkeiba_jockey_id, time, diff, passing, 
                final_furlong_time, win_odds, favorite, weight, trainer,
                netkeiba_trainer_id, owner, netkeiba_owner_id, prize):
        query = "insert into raw_race_results values (null," + "%s,"*21 +"%s)"
        params = [raw_race_id, rank, frame_number, horse_number, horse_name, netkeiba_horse_id]
        params += [horse_gender_age, carried_weight, jockey_name, netkeiba_jockey_id, time, diff, passing]
        params += [final_furlong_time, win_odds, favorite, weight, trainer, netkeiba_trainer_id]
        params += [owner, netkeiba_owner_id, prize]
        return self.conn.execute(query, *params)