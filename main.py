import random

import nltk
import sklearn

import analysis
import data_cleaning
import data_collection as dc
import json

import utils
from sentiment import SentimentAnalyser


def collect_tweets():
    with open('config.json', 'r') as f:
        config = json.load(f)

    d = dc.DataCollection(config)
    d.collect_tweets('output', 'a')


def tokenize_pos_dataset():
    with open('dataset.json', 'r', encoding='utf8') as f:
        dataset = json.load(f)

    i = 4
    step = int(len(dataset) / 4)
    dataset = dataset[i * step: (i + 1) * step]

    for e, t in enumerate(dataset):
        tokens = nltk.word_tokenize(t['t'])
        pos = nltk.pos_tag(tokens)

        t['tokens'] = tokens
        t['pos'] = pos

        print(e, len(dataset))

    with open('dataset_lex_sentiment_result.json_' + str(i), 'w', encoding='utf8') as f:
        json.dump(dataset, f, ensure_ascii=False)


def merge_tokenize_pos_dataset():
    merged_dataset = []
    for i in range(5):
        with open('dataset_lex_sentiment_result.json_' + str(i), 'r', encoding='utf8') as f:
            dataset = json.load(f)
            merged_dataset.extend(dataset)

    with open('dataset_token_pos.json', 'w', encoding='utf8') as f:
        json.dump(merged_dataset, f, ensure_ascii=False)


def run_sentiment_analysis():
    with open('dataset_token_pos.json', 'r', encoding='utf8') as f:
        dataset = json.load(f)

    i = 4
    step = int(len(dataset) / 4)
    dataset = dataset[i * step: (i + 1) * step]

    model = SentimentAnalyser()
    for e, t in enumerate(dataset):
        score, label = model.predict(t['t'], t['pos'])
        t['ss'] = score
        t['sl'] = label

        del t['tokens']
        del t['pos']

        print(e, len(dataset))

    with open('dataset_lex_sentiment_result.json' + str(i), 'w', encoding='utf8') as f:
        json.dump(dataset, f, ensure_ascii=False)


def merge_run_sentiment_analysis():
    merged_dataset = []
    for i in range(5):
        with open('dataset_lex_sentiment_result.json' + str(i), 'r', encoding='utf8') as f:
            dataset = json.load(f)
            merged_dataset.extend(dataset)

    with open('dataset_lex_sentiment_result.json', 'w', encoding='utf8') as f:
        json.dump(merged_dataset, f, ensure_ascii=False)


def sample_from_dataset():
    with open('dataset.json', 'r', encoding='utf8') as f:
        dataset = json.load(f)

    samples = random.sample(dataset, 30)

    for s in samples:
        s['label'] = 'None'

    with open('sample.json', 'w', encoding='utf8') as f:
        json.dump(samples, f, ensure_ascii=False)


def eval():
    with open('dataset_lex_sentiment_result.json', 'r', encoding='utf8') as f:
        dataset = json.load(f)

    the_map = {}
    for i in dataset:
        the_map[i['i']] = i['sl']

    with open('sample.json', 'r', encoding='utf8') as f:
        samples = json.load(f)

    for s in samples:
        s['pred'] = the_map[s['i']]

    pred = []
    gold = []
    for t in samples:
        pred.append(1 if t['pred'] == 'positive' else 0)
        gold.append(1 if t['label'] == 'positive' else 0)

    print(sklearn.metrics.accuracy_score(pred, gold))
    print(sklearn.metrics.precision_score(pred, gold))
    print(sklearn.metrics.recall_score(pred, gold))


if __name__ == '__main__':
    # run_sentiment_analysis()
    # tokenize_pos_dataset()
    # merge_tokenize_pos_dataset()
    # merge_run_sentiment_analysis()
    # utils.ground_truth_dataset("output")
    # analysis.generate_analysis_file()
    # analysis.create_bar_chart_sentiments()
    # analysis.create_bar_chart_sentiments_aggregate()
    # analysis.create_stack_pos_vs_neg()
    # analysis.create_stack_pos_to_neg()
    # analysis.create_count()

    # sample_from_dataset()
    eval()
