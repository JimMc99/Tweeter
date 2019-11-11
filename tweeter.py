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
    def __init__(self, fpath):
        self.fpath = fpath

        self.markov_model_fo = defaultdict(lambda: Counter())
        self.start_words = Counter()
        self.__load_model()

    def __load_model(self):
        # load model (prepare data)
        # first-order markov model of words (no preprocessing)
        # each token key goes to a Counter value containing counts of the subsequent word
        # to add to this model, markov_model_fo[current_word][next_word] += 1
        tweets = list_lines(self.fpath)

        for tweet in tweets:
            tokens = tweet.split()

            # add each token except the last token in the tweet to the markov model
            for i, token in enumerate(tokens[:-1]):
                self.markov_model_fo[token][tokens[i + 1]] += 1
            # for the last token, nothing follows
            if len(tokens):
                self.markov_model_fo[tokens[-1]][None] += 1
                self.start_words[tokens[0]] += 1

    def new_tweet(self):
        # create new tweet from model
        new_tweet_list = []

        start_keys = list(self.start_words.keys())
        start_values = list(self.start_words.values())
        start_word = random.choices(start_keys, weights=start_values)[0]

        current_word = start_word

        while current_word is not None:
            new_tweet_list.append(current_word)

            next_keys = list(self.markov_model_fo[current_word].keys())
            next_values = list(self.markov_model_fo[current_word].values())
            next_word = random.choices(next_keys, weights=next_values)[0]

            current_word = next_word

        return ' '.join(new_tweet_list)


if __name__ == "__main__":
    trump_tweeter = Tweeter('trump_tweets.txt')
    print(trump_tweeter.new_tweet())
