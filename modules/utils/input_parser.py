from re import compile

PUNCTUATION = frozenset('.,!?:')  # This needs better home


class InputParser:
    def __init__(self, stream, *args, **kwargs):
        """
        InputParser(stream[, ...], re=*, output_newlines=False)

            Parses input from stream into words utilising regular expressions

            Parameters
            -----------
            stream : iterable of strings or multiple strings
                The source of life
            re : string
                Regular expression that should match words in the text
            output_newlines : bool
                Return '\\n' after every line
        """
        self.re = compile(kwargs.get('re', r'[A-Za-z]+|\.'))
        self.output_newlines = kwargs.get('output_newlines', False)
        if len(args) > 0:
            self.stream = (stream,) + args
        else:
            self.stream = stream

    def next_word(self):
        """
        next_word()

            Iterator for words

            Returns
            --------
            word: string
                Parsed word
        """
        for line in self._next_line():
            for match in self.re.finditer(line):
                yield match[0]
            if self.output_newlines:
                yield '\n'

    def _next_line(self):
        for line in self.stream:
            yield line
