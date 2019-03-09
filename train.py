from modules.trainer import Trainer
from argparse import ArgumentParser
from os import scandir
from sys import stdin

re_nums_words_punc = r'[\w\d]+(?:[\-\'][\w\d]+)*|[\.!\?]'
re_words_punc = r'[\w]+(?:[\-\'][\w]+)*|[\.!\?]'
re_ru_words = r'[А-Яа-яёЁ]+(?:[\-\'][А-Яа-яёЁ]+)*'
re_ru_words_punc = r'[А-Яа-яёЁ]+(?:[\-\'][А-Яа-яёЁ]+)*|[\.\?!]'


def parse_args():
    arg_parser = ArgumentParser(description='Trains the model')
    arg_parser.add_argument('--model',
                            help='Path to model file',
                            required=True)
    arg_parser.add_argument('--input-dir',
                            help='Directory with .txt files for input')
    arg_parser.add_argument('--model-n',
                            help='Model parameter n',
                            default=2,
                            type=int)
    arg_parser.add_argument('--lc',
                            help='Convert strings to lowercase',
                            action='store_true')
    vk_group = arg_parser.\
        add_argument_group(title='VK Parsing',
                           description='Gets posts from vk group.\n'
                                       'If used, other input is ignored.'
                                       'Group name, login and '
                                       'password are mutually required')
    vk_group.add_argument('--vk-group-name',
                          help='URL name of the group to parse')
    vk_group.add_argument('--vk-login', help='VK Login')
    vk_group.add_argument('--vk-pass', help='VK Password')
    vk_group.add_argument('--vk-appid', help='VK API AppID',
                          default=5181634, type=int)
    vk_group.add_argument('--vk-count',
                          help='Post count to parse (defaults to all)',
                          default=-1, type=int)
    vk_group.add_argument('--vk-offset', help='Post parsing offset',
                          default=0, type=int)
    vk_group.add_argument('--vk-file',
                          help='If specified, dumps posts '
                               'into file and returns')
    args = arg_parser.parse_args()
    if args.vk_group_name is not None and (args.vk_login is None or args.vk_pass is None):
        arg_parser.error("VK login and password are required with --vk-group-name parameter")
    return args


def main():
    args = parse_args()

    if args.vk_group_name is not None:
        from modules import VKParser
        vk_parser = VKParser(group_name=args.vk_group_name,
                             app_id=args.vk_appid,
                             login=args.vk_login,
                             password=args.vk_pass)
        if args.vk_file is not None:
            vk_parser.dump_posts(args.vk_file)
            return

    trainer = Trainer(n=args.model_n, lc=args.lc)

    if args.vk_group_name is not None:
        trainer.train(vk_parser.post_iter(args.vk_offset, args.vk_count),
                      re=re_ru_words_punc,
                      output_newlines=True)
    elif args.input_dir is not None:
        for entry in scandir(args.input_dir):
            if entry.name.endswith('.txt') and entry.is_file():
                with open(entry.path, 'r', encoding='utf8') as file:
                    trainer.train(file, re=re_ru_words_punc,
                                  output_newlines=True)
    else:
        trainer.train(stdin, re=re_ru_words_punc, output_newlines=True)

    with open(args.model, 'wb') as file:
        trainer.get_model().dump(file)


if __name__ == '__main__':
    main()
