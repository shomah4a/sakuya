#-*- coding:utf-8 -*-

import sys
import argparse

from sakuya.model import session, functions
from sakuya.cui import output



def make_parser():

    parser = argparse.ArgumentParser(description='Java type searcher')

    parser.add_argument('types', metavar='TYPES', type=str, nargs='+',
                        help='types for serach (ex: Integer Integer String)')

    parser.add_argument('--format', '-f', metavar='FMT', type=str,
                        help='output format(normal/json)')

    parser.add_argument('--dbfile', '-d', metavar='FILE', type=str,
                        default='data.db', help='sqlite database(default: data.db)')

    parser.add_argument('--verbose', '-v', action='store_true',
                        default=False, help='print full qualified package name')


    return parser



def main(args=sys.argv[1:]):

    parser = make_parser()

    opts = parser.parse_args(args)

    rtype = opts.types[-1]
    args = opts.types[:-1]

    session.initialize('sqlite:///' + opts.dbfile)

    with session.Session() as sess:
        results = functions.search_by_type(sess, rtype, args)
        output.print_result(results, opts)





if __name__ == '__main__':
    main()


