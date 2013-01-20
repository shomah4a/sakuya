#-*- coding:utf-8 -*-

import setuptools
import sakuya as pkg

pkgname = pkg.__name__

setuptools.setup(
    name=pkgname,
    version=pkg.__version__,
    packages=[pkgname],
    install_requires=[
        'sqlalchemy',
        'pygments',
        'simplejson',
        'WebOb',
        'WebDispatch',
        'zope.pagetemplate',
        ],
    author=pkg.__author__,
    license=pkg.__license__,
    url='https://github.com/shomah4a/sakuya',
    description=u'木花之佐久夜毘売, the goddess who appears in Japanese mythology.',
    long_description=pkg.__doc__,
    entry_points={
        'console_scripts':['sakuya=sakuya.cui:main',
                           'serve=sakuya.web:main',
                           'sakuya_build=sakuya:main'],
        },
    classifiers='''
Programming Language :: Python
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Utilities
'''.strip().splitlines())

