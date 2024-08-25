from .connection import Connection

class RawRaceInformationDao(object):
    def __init__(self, conn:Connection):
        self.conn = conn

    def insert(self, raw_race_id, race_number, race_condition, 
                weather, track_condition, starting_time, race_date, 
                event_name, race_class, race_type):
        query = "insert into raw_race_informations values (null," + "%s,"*9 + "%s)"
        params = [raw_race_id, race_number, race_condition, weather, track_condition]
        params += [starting_time, race_date, event_name, race_class, race_type]
        return self.conn.execute(query, *params)