from nltk.corpus import sentiwordnet as swn
from nltk import word_tokenize, pos_tag


class SentimentAnalyser:
    def __init__(self):
        pass

    def predict(self, text, pos=None):
        score = self.sentiwordnet_lexicon(text, pos)
        label = self.get_label(score)

        return score, label

    def sentiwordnet_lexicon(self, text, pos):
        if not pos:
            tokens = word_tokenize(text)
            tagged_text = pos_tag(tokens)
        else:
            tagged_text = pos

        pos_score, neg_score, found_token_count, obj_score = [0] * 4
        for word, tag in tagged_text:
            ss_set = None
            if 'NN' in tag and list(swn.senti_synsets(word, 'n')):
                ss_set = list(swn.senti_synsets(word, 'n'))[0]
            elif 'VB' in tag and list(swn.senti_synsets(word, 'v')):
                ss_set = list(swn.senti_synsets(word, 'v'))[0]
            elif 'JJ' in tag and list(swn.senti_synsets(word, 'a')):
                ss_set = list(swn.senti_synsets(word, 'a'))[0]
            elif 'RB' in tag and list(swn.senti_synsets(word, 'r')):
                ss_set = list(swn.senti_synsets(word, 'r'))[0]

            if ss_set:
                pos_score += ss_set.pos_score()
                neg_score += ss_set.neg_score()
                obj_score += ss_set.obj_score()
                found_token_count += 1

        if found_token_count == 0:
            return 0

        final_score = (1 * pos_score - 1.07 * neg_score)
        norm_final_score = round(float(final_score) / found_token_count, 2)

        return norm_final_score

    def get_label(self, norm_score):
        return 'positive' if norm_score >= 0 else 'negative'
