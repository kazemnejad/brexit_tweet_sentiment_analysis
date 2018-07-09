import json
import os
import random

import sys
import tweepy
import twitter


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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

        if len(list(os.listdir(output_dir))) > 0:
            last_buffered = max([int(i) for i in os.listdir(output_dir)]) + 1
        else:
            last_buffered = 0

        last_id_index = self.find_last_tweet(tweets_ids, output_dir)
        print(last_id_index)
        eprint(last_id_index)
        print(last_id_index)

        tweets_ids = tweets_ids[last_id_index:]

        for i in range(int(len(tweets_ids) / 100) + 1):
            # if i * 100 < last_buffered * buffer_size:
            #     eprint("skipped", i * 100)
            #     continue

            ids = [i[0] for i in tweets_ids[i * 100: (i + 1) * 100]]

            tweets = []
            isDone = False
            while not isDone:
                try:
                    tweets = api.statuses_lookup(ids, False, True)
                    isDone = True
                except:
                    eprint("retrying...")
                    isDone = False
                    continue

            eprint("#", (i + 1) * 100, len(tweets_ids))

            buffer.extend(tweets)

            if len(buffer) >= buffer_size:
                self.save_buffer(buffer, output_dir)
                buffer = []

    def find_last_tweet(self, tweets_ids, output_dir):
        if len(list(os.listdir(output_dir))) > 0:
            last_buffered = max([int(i) for i in os.listdir(output_dir)])
        else:
            return 0

        with open(os.path.join(output_dir, str(last_buffered)), 'r') as f:
            buffer = json.load(f)

        last_id = buffer[-1].i

        for i in range(len(tweets_ids)):
            if tweets_ids[i][0] == last_id:
                return i + 1

        return 0

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
