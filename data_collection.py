import json
import os
import random

import sys
import tweepy
import twitter


class DataCollection:
    def __init__(self, config):
        self.config = config

        self.init_api()

    def init_api(self):
        api_key = self.config['apiKey']['keys'][self.config['apiKey']['index']]
        self.api = twitter.Api(consumer_key=api_key['consumer_key'],
                               consumer_secret=api_key['consumer_secret'],
                               access_token_key=api_key['access_token'],
                               access_token_secret=api_key['access_token_secret'])

    def collect(self):
        results = self.api.GetSearch(
            raw_query="q=threelions%20&result_type=recent&since=2014-07-19&count=1000", )

        # raw_query="q=%23apple%20since%3A2017-07-19%20until%3A2017-10-17")

    def collect_tweets(self, base_dir, output_dir):
        is_first_half = self.config['ifh']

        tweets_ids = []
        for name in os.listdir(base_dir):
            with open(os.path.join(base_dir, name), 'r') as f:
                ids = [(l[:-1].split()[0], name) for l in f]
                if is_first_half:
                    ids = ids[: int(len(ids) / 2)]
                else:
                    ids = ids[int(len(ids) / 2):]

                tweets_ids.extend(ids)

        api_key = self.config['apiKey']['keys'][self.config['apiKey']['index']]

        # Twitter API credentials
        consumer_key = api_key["consumer_key"]
        consumer_secret = api_key["consumer_secret"]
        access_key = api_key["access_token"]
        access_secret = api_key["access_token_secret"]

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=1000,
                         retry_errors=[503], retry_delay=1)

        buffer = []
        buffer_size = 10 * 100

        for i in range(int(len(tweets_ids) / 100) + 1):
            ids = [i[0] for i in tweets_ids[i * 100: (i + 1) * 100]]

            tweets = api.statuses_lookup(ids, False, True)
            buffer.extend(tweets)

            print("#", (i + 1) * 100, len(tweets_ids))

            if len(buffer) >= buffer_size:
                self.save_buffer(buffer, output_dir)
                buffer = []

    def save_buffer(self, buffer, output_dir):
        trim_tweets = [{
            "i": t.id,
            "t": t.text,
            "u": t.user.id,
            "d": str(t.created_at),
            "l": t.lang
        } for t in buffer]

        if len(list(os.listdir(output_dir))) > 0:
            output_filename = max([int(i) for i in os.listdir(output_dir)]) + 1
        else:
            output_filename = 0
        with open(os.path.join(output_dir, str(output_filename)), 'w', encoding='utf8') as f:
            json.dump(trim_tweets, f, ensure_ascii=False)
