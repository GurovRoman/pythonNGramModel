import pickle
from collections import defaultdict, Counter
from numpy.random import choice


class Model:
    def __init__(self, **kwargs):
        """
        Model(n=2, min_n=1)

            Implements the n-gram model.
            Supports variable length occurrences

            Parameters
            -----------
            n : int
                Maximum length of n-grams.
            min_n : int
                Minimum length of n-grams.

            Special words
            --------------
            Words that are considered special:
                '' : No word at all. Used for
                     storing n-grams with length < n
                '_' : Text beginning padding word

        """
        self._n = kwargs.get('n', 2)
        self._min_n = kwargs.get('min_n', 1)
        # All the occurrences are stored with length = n
        #
        self._indexed_word_data = defaultdict(Counter)
        # And the words are indexed in integers
        self._word_index = WordIndex()

        self._word_index.add_word('')
        self._word_index.add_word('_')

        assert(0 < self._min_n <= self._n)

    def get_n(self):
        return self._n

    def get_min_n(self):
        return self._min_n

    def load(self, file, method='pickle'):
        """
        load(file, method='pickle')

            Loads model from file

            Parameters
            -----------
            file : file object
                Stream to load from
            method : string
                The way the model is stored
                    pickle : Plain pickled object
        """
        if method == 'pickle':
            self.__dict__.update(pickle.load(file).__dict__)
        else:
            raise ValueError(f'Unknown serialization method: \'{method}\'')

    def dump(self, file, method='pickle'):
        """
        dump(file, method='pickle')

            Dumps model to a file

            Parameters
            -----------
            file : file object
                Stream to dump to
            method : string
                The way the model will be stored
                    pickle : Plain pickled object
        """
        if method == 'pickle':
            pickle.dump(self, file)
        else:
            raise ValueError(f'Unknown serialization method: \'{method}\'')

    def add_occurrence(self, occurrence):
        """
        add_occurrence(occurrence)

            Adds the occurrence into model.
            Also, recursively adds all the suffixes
            with length >= min_n

            Parameters
            -----------
            occurrence : tuple
                Tuple of words to add
        """
        self._add_occurrence(occurrence)

    def get_prediction(self, previous, min_n=None):
        """
        get_prediction(previous, min_n=None):

            Predicts the next word based on previous ones.
            If there is no possible prediction, recursively
            tries to predict from suffixes with length >= min_n

            Parameters
            -----------
            previous : tuple
                Tuple of words to predict next word for
            min_n : int
                Override model's min_n parameter (can't be less)

            Returns
            --------
            prediction: string
                Equals '\\n' if there is no possible prediction
        """
        return self._get_prediction(previous, min_n)

    def _add_occurrence(self, occurrence, indexed_input=False):
        # Make tuple indexed if not
        if not indexed_input:
            occurrence = tuple(map(self._word_index.add_word, occurrence))

        # Pad the occurrence to match n
        n_difference = self._n - len(occurrence)
        assert(n_difference >= 0)
        occurrence_padded = (self._word_index.get_index(''),) * n_difference + occurrence

        self._indexed_word_data[occurrence_padded[:-1]][occurrence[-1]] += 1
        # Add suffix with len = n - 1
        if len(occurrence) > self._min_n:
            self._add_occurrence(occurrence[1:], indexed_input=True)

    def _get_prediction(self, previous, min_n=None, indexed_input=False):
        # Make tuple indexed if not
        if not indexed_input:
            previous = tuple(map(self._word_index.add_word, previous))

        if min_n is None:
            min_n = self._min_n
        assert(self._min_n <= min_n <= self._n)

        # Pad the previous to match n - 1
        difference = self._n - (len(previous) + 1)
        assert(difference >= 0)
        previous_padded = (self._word_index.get_index(''),) * difference + previous

        candidates = self._indexed_word_data[previous_padded]
        if len(candidates) == 0:
            if len(previous) < min_n:
                return '\n'
            else:
                return self._get_prediction(previous[1:], min_n=min_n, indexed_input=True)

        candidates, counts = zip(*candidates.items())
        full_sum = sum(counts)
        candidates_prob = [i / full_sum for i in counts]
        return self._word_index.get_word(choice(candidates, p=candidates_prob))


class WordIndex:
    def __init__(self):
        """
        WordIndex()

            Indexes words as integers. Quite self-explanatory
        """
        self.index_to_word = []
        self.word_to_index = {}

    def get_word(self, index):
        return self.index_to_word[index]

    def get_index(self, word):
        return self.word_to_index[word]

    def add_word(self, word):
        index = self.word_to_index.get(word)
        if index is None:
            self.index_to_word.append(word)
            index = len(self.index_to_word) - 1
            self.word_to_index[word] = index
        return index
