from modules import Generator, Model
from textwrap import wrap
from argparse import ArgumentParser
from sys import stdout


def parse_args():
    arg_parser = ArgumentParser(description='Generates text using the model')
    arg_parser.add_argument('--model', help='Path to model file', required=True)
    arg_parser.add_argument('--length', help='Text length in words', required=True, type=int)
    arg_parser.add_argument('--seed', help='First word in the text')
    arg_parser.add_argument('--count', help='Output more than one text', type=int, default=1)
    arg_parser.add_argument('--n', help='n to use', type=int)
    arg_parser.add_argument('--min-n', help='Minimum n to use', type=int)
    arg_parser.add_argument('--break-on-end', help='End text if sentence has ended', action='store_true')
    arg_parser.add_argument('--output', help='Output file')
    arg_parser.add_argument('--wrap', help='Wrap output strings', action='store_true')
    return arg_parser.parse_args()


def main():
    args = parse_args()

    model = Model()
    with open(args.model, 'rb') as file:
        model.load(file)

    generator = Generator(model)

    if args.output is not None:
        file = open(args.output, 'a', encoding='utf-8')
    else:
        file = stdout

    for i in range(0, args.count):
        text = generator.generate(args.length, seed=args.seed,
                                  min_n=args.min_n, n=args.n,
                                  break_on_end=args.break_on_end)
        if args.wrap:
            text = '\n'.join(wrap(text))
        print(text, '\n', file=file)

    if args.output is not None:
        file.close()


if __name__ == '__main__':
    main()
