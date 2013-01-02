#-*- coding:utf-8 -*-

from __future__ import with_statement

__version__ = '0.1.0'
__author__ = '@shomah4a'
__license__ = 'GPLv3'


def main():

    from .model import session

    session.initialize('sqlite:///data.db')


    from .model import functions
    from . import jython

    # jython.run_jython(['java.util'], functions.create_from_json)

    with session.Session() as sess:

        functions.search_by_type(sess, 'void', ['Object[]'])
        functions.search_by_type(sess, 'void', [])




