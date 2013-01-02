#-*- coding:utf-8 --*-


from pygments import lexers, token

from sakuya.parser import model, utils


def parse(filepath):

    tokens = model.Token.mk_tokens(get_tokens(filepath))

    n_start, pkg = get_package(tokens)

    return pkg



def get_package(tokens):
    u'''
    Java のパッケージ名を取得
    '''

    names = []
    in_pkg = False

    index = 0

    for idx, tok in enumerate(tokens, 0):

        if in_pkg:

            if tok.type == token.Operator and tok.text == u';':
                return idx+1, '.'.join(names)

            if tok.type in token.Name:
                names.append(tok.text)

        if tok.type == token.Keyword.Namespace:
            print 'found package'
            in_pkg = True




def parse_class(tokens, start):
    u'''
    class を解析する
    '''

    start = utils.find_next(tokens, start, Token.Keyword.Declaration, 'class')





def get_tokens(filepath):

    lexer = lexers.get_lexer_for_filename(filepath)

    with open(filepath) as fp:

        return list(lexer.get_tokens(fp.read()))




