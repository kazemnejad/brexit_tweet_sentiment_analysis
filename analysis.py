import json
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime

import utils


def generate_analysis_file():
    gold = utils.ground_truth_dataset('output')

    buckets = {str(i): {
        'sum_score': 0,
        'count': 0,
        'pos_count': 0,
        'neg_count': 0,
        'neut_count': 0
    } for i in os.listdir('output')}

    with open('dataset_lex_sentiment_result.json', 'r', encoding='utf8') as f:
        dataset = json.load(f)

    for e, t in enumerate(dataset):
        time_label = gold[str(t['i'])][0]

        bucket = buckets[time_label]

        bucket['count'] += 1
        bucket['sum_score'] += t['ss']

        if t['ss'] != 0:
            if t['sl'] == 'positive':
                bucket['pos_count'] += 1
            else:
                bucket['neg_count'] += 1
        else:
            bucket['neut_count'] += 1

    with open('analysis.json', 'w') as f:
        json.dump(buckets, f)


def aggregate_by_date(buckets):
    new_buckets = {}
    for d, b in buckets.items():
        date_str, hour = d.split('_')

        new_bucket = new_buckets.get(date_str, {
            'sum_score': 0,
            'count': 0,
            'pos_count': 0,
            'neg_count': 0,
            'neut_count': 0
        })

        b['sum_score'] = b['sum_score'] / b['count']

        for k in b:
            new_bucket[k] += b[k]

        new_buckets[date_str] = new_bucket

    return new_buckets


def create_bar_chart_sentiments():
    with open('analysis.json', 'r') as f:
        buckets = json.load(f)

    x = []
    avg = []
    for d, bucket in buckets.items():
        date_str, hour = d.split('_')
        y, m, d = date_str.split('-')
        x.append(datetime.datetime(int(y), int(m), int(d), int(hour), 0, 0))

        avg.append(bucket['sum_score'] / bucket['count'])

    print(len(x))

    plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    ax.bar(x, avg, width=0.05, align='edge', )
    ax.xaxis_date()

    plt.show()


def create_bar_chart_sentiments_aggregate():
    with open('analysis.json', 'r') as f:
        buckets = aggregate_by_date(json.load(f))

    x = []
    avg = []
    for d, bucket in buckets.items():
        y, m, d = d.split('-')
        x.append(datetime.datetime(int(y), int(m), int(d), 0))

        avg.append(bucket['sum_score'] / 24)

    print(len(x))

    plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    ax.bar(x, avg)
    ax.xaxis_date()

    plt.show()


def create_stack_pos_vs_neg():
    with open('analysis.json', 'r') as f:
        buckets = aggregate_by_date(json.load(f))

    x = []
    pos = []
    neg = []
    for d, bucket in buckets.items():
        y, m, d = d.split('-')
        x.append(datetime.datetime(int(y), int(m), int(d), 0))

        pos.append(bucket['pos_count'] * 1.0 / bucket['count'])
        neg.append(bucket['neg_count'] * -1.0 / bucket['count'])

    plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    ax.bar(x, pos)
    ax.bar(x, neg, color='#d62728')
    ax.xaxis_date()

    plt.show()


def create_stack_pos_to_neg():
    with open('analysis.json', 'r') as f:
        buckets = aggregate_by_date(json.load(f))

    x = []
    pos = []
    neg = []
    for d, bucket in buckets.items():
        y, m, d = d.split('-')
        x.append(datetime.datetime(int(y), int(m), int(d), 0))

        pos.append(bucket['pos_count'] * 1.0 / bucket['neg_count'])

    plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    ax.bar(x, pos)
    ax.xaxis_date()

    plt.show()


def create_count():
    with open('analysis.json', 'r') as f:
        buckets = aggregate_by_date(json.load(f))

    x = []
    pos = []
    neg = []
    for d, bucket in buckets.items():
        y, m, d = d.split('-')
        x.append(datetime.datetime(int(y), int(m), int(d), 0))
        pos.append(bucket['count'])

    plt.figure(figsize=(20, 3))
    ax = plt.subplot(111)
    ax.bar(x, pos)
    ax.xaxis_date()

    plt.show()
