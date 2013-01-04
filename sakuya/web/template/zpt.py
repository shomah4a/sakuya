#-*- coding:utf-8 -*-
u'''
zpt を扱う
'''

import os

from zope.pagetemplate import pagetemplate

from sakuya.web import template


class ZPTPath(object):
    u'''
    zpt をレンダリングする際に使うパス情報をもったクラス
    '''


    EXTENSION = '.zpt'

    def __init__(self, path):

        self.path = path


    def get_current_dir(self):

        if os.path.isdir(self.path):
            return self

        return os.path.dirname(self.path)


    def __getattr__(self, attr):
        '''
        属性
        '''

        if attr in self.__dict__:
            return self.__dict__[attr]

        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


    def __getitem__(self, key):
        u'''
        / でアクセスしたときの情報
        '''

        cur = self.get_current_dir()

        joined = os.path.join(cur, key)

        if os.path.isdir(joined):
            return ZPTPath(joined)

        with_ext = joined + self.EXTENSION

        if os.path.exists(with_ext):
            return ZPTTemplate(joined)



class ZPTTemplate(ZPTPath, pagetemplate.PageTemplate):
    u'''
    zpt でレンダリングする
    '''

    def __init__(self, path):

        pagetemplate.PageTemplate.__init__(self)
        ZPTPath.__init__(self, path)

        with_ext = path + self.EXTENSION

        with file(with_ext) as fp:
            self.write(fp.read().decode('utf-8'))


    def pt_getContext(self, args=(), options=None, context=None, **kw):
        u'''
        オプション変数を渡す
        '''

        options = {} if options is None else options.copy()

        rval = pagetemplate.PageTemplate.pt_getContext(self, args, **kw)
        options.update(rval)

        options['here'] = self

        return options



class Context(dict):


    def __getattr__(self, key):

        if key in self:
            return self[key]

        return super(Context, self).__getattr__(key)




def rendering(filepath, context):
    u'''
    レンダリングする

    :param str filepath: テンプレートファイルのパス(拡張子抜き)
    :param dict context: コンテキスト情報
    :return: レンダリング結果
    :rtype: unicode
    '''

    tmpldir = template.get_template_dir()

    path = os.path.join(tmpldir, filepath)

    tmpl = ZPTTemplate(path)

    return tmpl(context=Context(context))


