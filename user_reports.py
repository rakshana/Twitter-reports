from time import time
from twython import TwythonStreamer
from urlparse import urlparse
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import json


class Streamer(TwythonStreamer):

    def __init__(self,  cred, time_limit, choice):
        super(Streamer, self).__init__(cred['consumer_key'], cred['consumer_secret'],
                                       cred['access_key'], cred['access_secret'])
        self.start_time = time()
        self.limit = time_limit
        self.minute = 1
        self.report = dict()
        self.report[self.minute] = dict()
        self.choice = choice
        self.stop_words = set(stopwords.words('english'))

    def on_success(self, data):
        if time() - self.start_time > self.limit:
            self.start_time = time()
            if choice == 1:
                self.print_user_report()
            elif choice == 2:
                self.print_links_report()
            elif self.choice == 3:
                self.print_content_report()
        if data['lang'] == 'en':
            self.process(data)

    def on_error(self, status_code, data):
        print 'Disconnected.'
        self.disconnect()

    def process(self, data):
        if self.choice == 1:
            user = data['user']['screen_name']
            if user not in self.report[self.minute]:
                self.report[self.minute][user] = 1
            else:
                self.report[self.minute][user] += 1
        elif self.choice == 2:
            links = data['entities']['urls']
            if links:
                for link in links:
                    domain = urlparse(link['expanded_url']).netloc
                    if domain not in self.report[self.minute]:
                        self.report[self.minute][domain] = 1
                    else:
                        self.report[self.minute][domain] += 1
        elif self.choice == 3:
            tweet = data['text']
            tokenizer = RegexpTokenizer(r'\w+')
            all_words = tokenizer.tokenize(tweet)
            for word in all_words:
                if word not in self.stop_words:
                    if word not in self.report[self.minute]:
                        self.report[self.minute][word] = 1
                    else:
                        self.report[self.minute][word] += 1
        else:
            self.on_error(400, data)

    def print_user_report(self):
        if self.minute >= 5:
            report_to_print = self.get_report()
        else:
            report_to_print = self.report[self.minute]
        if report_to_print == {}:
            print 'No tweers this round'
        else:
            for user in report_to_print:
                print user + ' tweeted ' + str(report_to_print[user]) + ' time(s).'
        self.refresh()

    def print_links_report(self):
        if self.minute >= 5:
            report_to_print = self.get_report()
        else:
            report_to_print = self.report[self.minute]
        if report_to_print == {}:
            print 'No tweets this round.'
        else:
            sorted_links = sorted(report_to_print, key=report_to_print.get, reverse=True)
            for link in sorted_links:
                print str(link) + ' : ' + str(report_to_print[link])
            # for link, count in sorted(report_to_print.iteritems(), key=lambda (k, v): (v, k)):
            #     print str(link) + ' : ' + str(count)
        self.refresh()

    def print_content_report(self):
        if self.minute >=5:
            report_to_print = self.get_report()
        else:
            report_to_print = self.report[self.minute]
        if report_to_print == {}:
            print 'No tweets this round.'
        else:
            sorted_words = sorted(report_to_print, key=report_to_print.get, reverse=True)
            for index, word in zip( range(10), sorted_words):
                print word + ' : ' + str(report_to_print[word])
        self.refresh()

    def get_report(self):
        aggregated_report = {}
        for i in range(self.minute-4, self.minute+1):
            for record in self.report[i]:
                if record not in aggregated_report:
                    aggregated_report[record] = self.report[i][record]
                else:
                    aggregated_report[record] += self.report[i][record]
        return aggregated_report

    def refresh(self):
        print '\n'
        self.minute += 1
        self.report[self.minute] = {}
        self.start_time = time()


if __name__ == '__main__':
    keyword = raw_input('Enter keyword : ')
    choice = int(raw_input('Would you like to see:\n1. User report\n2.Link report\n3.Content report\nEnter 1 or 2 : '))
    if keyword:
        with open("twitter_credentials.json", "r") as access_keys:
            credentials = json.load(access_keys)
        conn = Streamer(cred=credentials, time_limit=60, choice=choice)
        conn.statuses.filter(track=keyword)
