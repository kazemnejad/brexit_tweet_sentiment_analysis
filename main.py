import data_collection as dc
import json

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    d = dc.DataCollection(config)
    d.collect_tweets('output', 'a')
