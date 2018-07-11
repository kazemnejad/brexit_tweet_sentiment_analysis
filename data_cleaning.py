import json
import os
import re

from datetime import datetime

RT = re.compile(r'^RT( )* @[A-Za-z0-9_-]*( )*:')
link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
mention = re.compile(r'@[A-Za-z0-9_-]*')


class Tweet:
    def __init__(self, data):
        self.data = data
        self.data['d'] = datetime.strptime(data['d'], '%Y-%m-%d %H:%M:%S')

    def __hash__(self):
        return hash(self.data['i'])

    def __eq__(self, other):
        return self.data['i'] == other.data['i']


def strip_links(text):
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], '')
    return text


def remove_mentions(text):
    return re.sub(mention, '', text)


def remove_rt(text):
    return re.sub(RT, '', text)


def read_sub_dataset(path):
    tweet_ids = set()
    for a in os.listdir(path):
        with open(os.path.join(path, a), 'r', encoding='utf8') as f:
            tweets = json.load(f)
            tweet_ids.update(set([Tweet(t) for t in tweets]))

    return tweet_ids


def clean_tweet_text(text):
    text = strip_links(text)
    text = remove_rt(text)
    text = remove_mentions(text)
    text = text.replace('#', '')
    text = text.replace('…', '')

    return text


def collect_tweet():
    a1 = read_sub_dataset('sentiment_dataset/1/a')
    a2 = read_sub_dataset('sentiment_dataset/2/a')

    a1.update(a2)

    tweets = list(a1)
    tweets = [t for t in tweets if t.data['l'] == 'en']
    tweets.sort(key=lambda x: x.data['d'])

    for t in tweets:
        t.data['t'] = clean_tweet_text(t.data['t'])

    tweets = [{
        'i': t.data['i'],
        't': t.data['t'],
        'd': str(t.data['d'])
    } for t in tweets]

    print(len(tweets))

    return tweets


def create_dataset():
    tweets = collect_tweet()

    with open('dataset.json', 'w', encoding='utf8') as f:
        json.dump(tweets, f, ensure_ascii=False)
