#-*- coding:utf-8 -*-

import sys

from sakuya.jython import dump



def get_targets(args):

    return args



def main(args=sys.argv[1:]):

    targets = get_targets(args)

    if not targets:
        print >> sys.stderr, 'not enough arguments. require java package names'
        return 1

    dump.dump_objects(args)


if __name__ == '__main__':

    sys.exit(main(sys.argv[1:]))





