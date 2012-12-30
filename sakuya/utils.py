#-*- coding:utf-8 -*-
u'''
ちょっと便利な機能郡
'''

import os


class SlotEqual(object):
    u'''
    __slots__ を見て同値チェックする
    '''

    def __eq__(self, other):
        u'''
        同値チェック
        '''

        if self is other:
            return True

        if not isinstance(self, type(other)):
            return False

        if self.__slots__ != other.__slots__:
            return False

        return all(getattr(self, slot) == getattr(other, slot)
                   for slot in self.__slots__)


    def __ne__(self, other):

        return not self.__eq__(other)



def walk(root, func):
    u'''
    ディレクトリを歩く
    '''

    for path, dirs, files in os.walk(root):
        for f in files:
            fullpath = os.path.join(path, f)
            func(fullpath)



