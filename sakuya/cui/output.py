#-*- coding:utf-8 -*-

import simplejson

from sakuya.model import functions


def format_modifiers(modifiers):

    return ' '.join(functions.map_modifiers(modifiers))



def print_result(results, opt):
    u'''
    結果の出力
    '''

    fmt = opt.format

    if fmt == 'json':
        format_json(results, opt)
    else:
        format_normal(results, opt)



def format_json(results, opt):
    u'''
    JSON で出す
    '''

    print simplejson.dumps(results)



def format_normal(results, opt):

    verbose = opt.verbose
    f = lambda n: format_name(n, verbose)

    for result in results:

        print format_modifiers(result['modifiers']),
        print f(result['return_type']),
        print f(result) + '(' + ', '.join(map(f, result['args'])) + ')'



def format_name(item, verbose=False):

    name = item['name']
    fqname = item['fully_qualified']

    if verbose:
        return fqname
    else:
        return name

