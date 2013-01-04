#-*- coding:utf-8 -*-

import os


def get_template_dir():
    u'''
    テンプレートのある場所
    '''

    return os.path.join(os.path.dirname(__file__), 'templates')
