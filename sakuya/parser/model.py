#-*- coding:utf-8 -*-
u'''
パースした結果のモデル定義
'''

from sakuya import utils



class Token(utils.SlotEqual):
    u'''
    トークン情報を持つ
    Pygments のトークンだけだと微妙に足りないので追加で情報を持たせる
    '''

    __slots__ = ['type', 'text', 'line', 'column']


    def __init__(self, type, text, line, column):

        self.type = type
        self.text = text
        self.line = line
        self.column = column



    def dump(self):
        u'''
        DB 登録用
        '''

        return dict(type=self.type,
                    identifier=self.text,
                    line=self.line,
                    column=self.column)



    @classmethod
    def mk_tokens(cls, tokens):
        u'''
        Pygments のトークンに対して変換処理
        '''

        column, line = 0, 0
        result = []


        for typ, text in tokens:

            tok = Token(typ, text, line, column)
            result.append(tok)

            column += len(text)

            if text == u'\n':
                line += 1
                column = 0

        return result



class Function(object):
    u'''
    関数定義
    '''

    def __init__(self, namespace, row, column, rtype, args, doc):

        self.namespace = namespace
        self.row = row
        self.column = column
        self.return_type = rtype
        self.args = args
        self.doc = doc




