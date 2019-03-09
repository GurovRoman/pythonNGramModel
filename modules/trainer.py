from .utils import Model
from .utils import InputParser, PUNCTUATION


class Trainer:
    def __init__(self, **kwargs):
        """
        Trainer(model=*, lc=True)

            Trains a model. Duh.

            Parameters
            -----------
            model : Model object
                Model to train.
                If not passed, constructs with passed kwargs.
            lc : bool
                Convert words to lowercase if true
        """
        self._lower_case = kwargs.get('lc', True)
        self._model = kwargs.get('model', Model(**kwargs))

    def train(self, parser, *args, **kwargs):
        """
        train(parser[, ...])

            Initiate the training process

            Parameters
            -----------
            parser : Parser object
                Must have next_word() method returning iterable.
                If it doesn't, InputParser object is constructed
                with passed arguments.
        """
        if not hasattr(parser, 'next_word'):
            parser = InputParser(parser, *args, **kwargs)

        n = self._model.get_n()

        current = ('_',) * n
        for word in parser.next_word():
            # Ignore consecutive punctuation
            if word in PUNCTUATION and current[-1] in PUNCTUATION:
                continue

            # If got newline, consider it as end of text and start from scratch
            if word == '\n':
                current = ('_',) * n
                continue

            if self._lower_case:
                word = word.lower()

            current = current[1:] + (word,)
            self._model.add_occurrence(current)

    def get_model(self):
        return self._model
