from time import time
from twython import TwythonStreamer
from urlparse import urlparse
import json


class Streamer(TwythonStreamer):

    def __init__(self,  cred, time_limit, choice):
        super(Streamer, self).__init__(cred['consumer_key'], cred['consumer_secret'],
                                       cred['access_key'], cred['access_secret'])
        self.start_time = time()
        self.limit = time_limit
        self.report = {}
        self.choice = choice

    def on_success(self, data):
        if time() - self.start_time > self.limit:
            self.start_time = time()
            if choice == 1:
                self.print_user_report()
            elif choice == 2:
                self.print_links_report()
        if data['lang'] == 'en':
            self.process(data)

    def on_error(self, status_code, data):
        print 'Disconnected.'
        self.disconnect()

    def process(self, data):
        if self.choice == 1:
            user = data['user']['screen_name']
            if user not in self.report:
                self.report[user] = {'count': 1}
            else:
                self.report[user]['count'] += 1
        elif self.choice == 2:
            links = data['entities']['urls']
            if links:
                for link in links:
                    domain = urlparse(link['expanded_url']).netloc
                    if domain not in self.report:
                        self.report[domain] = 1
                    else:
                        self.report[domain] += 1

    def print_user_report(self):
        if self.report == {}:
            print 'No one tweeted in the last 1 minute.'
        else:
            for user in self.report:
                print user + ' tweeted ' + str(self.report[user]['count']) + ' time(s).'
        print '\n'
        self.report = {}

    def print_links_report(self):
        if self.report == {}:
            print 'No one tweeted links in the last one minute'
        else:
            for link, count in sorted(self.report.iteritems(), key=lambda (k, v): (v, k)):
                print str(link) + ' : ' + str(count)
        print '\n'
        self.report = {}


if __name__ == '__main__':
    keyword = raw_input('Enter keyword : ')
    choice = int(raw_input('Would you like to see:\n1. User report\n2.Link report\nEnter 1 or 2 : '))
    if keyword:
        with open("twitter_credentials.json", "r") as access_keys:
            credentials = json.load(access_keys)
        conn = Streamer(cred=credentials, time_limit=60, choice=choice)
        conn.statuses.filter(track=keyword)
