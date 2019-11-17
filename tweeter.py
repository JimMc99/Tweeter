from collections import Counter, defaultdict
import random


def list_lines(fpath):
    """
    Converts a text file to a list split by lines.
    :param fpath: filepath of text file
    :return: list of lines of text file
    """
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        return f.readlines()


class Tweeter:
    def __init__(self, fpath, model_order=2):
        self.fpath = fpath

        self.model_order = model_order  # length of ngrams the model looks at to find next word
        self.markov_model = defaultdict(lambda: Counter())
        self.start_ngrams = Counter()
        self.__load_model()

    def __load_model(self):
        # load model (prepare data)
        # nth order (depends on self.model_order) markov model of words (no preprocessing)
        # to add to this model, markov_model[current_ngram][next_word] += 1
        tweets = list_lines(self.fpath)

        for tweet in tweets:
            tokens = tweet.split()

            # add each ngram except the last ngram in the tweet to the markov model
            for i in range(len(tokens[:-self.model_order])):
                current_ngram = tuple(tokens[i:i+self.model_order])
                next_word = tokens[i + self.model_order]
                self.markov_model[current_ngram][next_word] += 1
            # for the last ngram, nothing follows
            if len(tokens) >= self.model_order:
                current_ngram = tuple(tokens[-self.model_order:])
                next_word = None
                self.markov_model[current_ngram][next_word] += 1

                start_ngram = tuple(tokens[:self.model_order])
                self.start_ngrams[start_ngram] += 1

    def new_tweet(self):
        # create new tweet from model
        new_tweet_list = []

        start_ngrams = list(self.start_ngrams.keys())
        start_values = list(self.start_ngrams.values())
        start_ngram = random.choices(start_ngrams, weights=start_values)[0]

        current_ngram = start_ngram

        while None not in current_ngram:
            new_tweet_list.append(current_ngram[0])

            next_words = list(self.markov_model[current_ngram].keys())
            next_values = list(self.markov_model[current_ngram].values())
            next_word = random.choices(next_words, weights=next_values)[0]

            current_ngram = tuple(current_ngram[1:] + (next_word,))
        new_tweet_list.extend(current_ngram[:-1])

        return ' '.join(new_tweet_list)


class TrumpTweeter(Tweeter):
    def __init__(self):
        super(TrumpTweeter, self).__init__(fpath='trump_tweets.txt')


if __name__ == "__main__":
    trump_tweeter = TrumpTweeter()
    print(trump_tweeter.new_tweet())
