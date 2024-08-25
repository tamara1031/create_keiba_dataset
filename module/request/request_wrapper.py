import time, requests
from urllib.parse import urlparse

class RequestWrapper(object):
    def __init__(self, request_interval_milli = 1000):
        self.request_interval_milli = request_interval_milli
        self.last_requested_at = 0

    def get(self, url):
        parsed_url = urlparse(url)

        target_epochmilli = self.last_requested_at + self.request_interval_milli
        self.sleep_until(target_epochmilli)

        response = requests.get(url)
        self.last_requested_at = time.time()*1000
        
        return response

    def sleep_until(self, target_epochmilli):
        epochmilli = time.time()*1000
        sleep_sec = (target_epochmilli - epochmilli)/1000
        if(sleep_sec > 0):
            time.sleep(sleep_sec)

