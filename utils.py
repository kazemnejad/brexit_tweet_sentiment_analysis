import random

import os


def sample_tweet_ids(divisor, base_dir, output_dir):
    for name in os.listdir(base_dir):
        print(name)
        with open(os.path.join(base_dir, name), 'r') as f:
            lines = [l[:-1] for l in f]
            sampled = random.sample(set(lines), int(len(lines) / divisor))

        with open(os.path.join(output_dir, name), 'w') as f:
            f.write("\n".join(sampled))


def ground_truth_dataset(base_dir):
    dataset = {}
    for name in os.listdir(base_dir):
        print(name)
        with open(os.path.join(base_dir, name), 'r') as f:
            lines = [l[:-1].split() for l in f]
            for id, label in lines:
                dataset[id] = (name, label)

    return dataset
