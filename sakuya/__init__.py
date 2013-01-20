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

    jython.run_jython(['com.arielnetworks'], functions.create_from_json)

    with session.Session() as sess:
        pass

        # functions.search_by_type(sess, 'void', ['List', 'Object'])
        # functions.search_by_type(sess, 'void', [])




