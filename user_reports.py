from time import time
from twython import TwythonStreamer
import json


class Streamer(TwythonStreamer):

    def __init__(self,  consumer_key, consumer_secret, access_key, access_secret, time_limit):
        super(Streamer, self).__init__(consumer_key, consumer_secret, access_key, access_secret)
        self.start_time = time()
        self.limit = time_limit
        self.report = {}

    def on_success(self, data):
        if time() - self.start_time > self.limit:
            self.start_time = time()
            self.print_and_refresh()
        if data['lang'] == 'en':
            self.process(data)

    def on_error(self, status_code, data):
        print 'Disconnected.'
        self.disconnect()

    def process(self, data):
        user = data['user']['screen_name']
        if user not in self.report:
            self.report[user] = 1
        else:
            self.report[user] += 1

    def print_and_refresh(self):
        if self.report == {}:
            print 'No one tweeted in the last 1 minute.'
        else:
            for user in self.report:
                print user + ' tweeted ' + str(self.report[user]) + ' time(s).'
        print '\n'
        self.report = {}


if __name__ == '__main__':
    keyword = raw_input('Enter keyword')
    if keyword:
        with open("twitter_credentials.json", "r") as file:
            credentials = json.load(file)
        conn = Streamer(credentials['consumer_key'], credentials['consumer_secret'],
                        credentials['access_key'], credentials['access_secret'], 60)

        conn.statuses.filter(track=keyword)
