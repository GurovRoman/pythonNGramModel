from .utils import PUNCTUATION


class Generator:

    def __init__(self, model, **kwargs):
        """
        Generator(model)

            Handles generation of text based on model

            Parameters
            -----------
            model : Model
        """
        self._model = model

    def generate(self, length, seed=None, n=None, min_n=None, break_on_end=False):
        """
        generate(length, seed=None, n=None, min_n=None, break_on_end=False)

            Generates text based on model

            Parameters
            -----------
            length : Model
                Length of generated text in words.
                Some parameters may allow shorter texts
            seed : string
                First word of the text
                If None, lets the model choose it
            n : integer
                Maximum n to use for generation
            min_n : integer
                Minimum n to use for generation
            break_on_end : bool
                Stops generation in model predicts '\\n'

            Returns
            --------
            text : string
                Generated text
        """
        if n is None:
            n = self._model.get_n()
        if min_n is None:
            min_n = self._model.get_min_n()
        current = ('_',) * (n - 2)
        text = ''
        word_count = 0
        if seed is None:
            current += ('_',)
        else:
            current += (seed,)
            text += seed
            word_count += 1

        while word_count < length:
            next_word = self._model.get_prediction(current, min_n=min_n)
            if next_word == '\n':
                if break_on_end:
                    break
                else:
                    text += '\n'
                    current = ('_',) * (n - 1)
                    continue
            if text != '' and not text.endswith(tuple(' \n')) and next_word not in PUNCTUATION:
                text += ' '
            text += next_word
            word_count += 1
            current = current[1:] + (next_word,)
        return text
