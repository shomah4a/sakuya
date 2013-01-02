#-*- coding: utf-8 -*-

import sqlalchemy as al
from sqlalchemy import sql
from sqlalchemy.sql import functions
from sqlalchemy.ext import declarative as decl


Base = decl.declarative_base()


class Type(Base):
    u'''
    型の名前と名前空間を保持

    :param int id: primary key
    :param str name: クラス名
    :param str fqname: パッケージ名まで含めた名前
    '''

    __tablename__ = 'types'
    __table_args__ = (
        al.UniqueConstraint('fqname', name='uc_fqname'),)

    id = decl.Column(al.Integer, primary_key=True, autoincrement=True)
    name = decl.Column(al.Unicode(255), nullable=False)
    fqname = decl.Column(al.Unicode(1024), nullable=False)



class Method(Base):
    u'''
    メソッド情報

    :param int id: primary key
    ;param int signature:
    :param str name: メソッド名
    :param str fqname: パッケージ名・クラス名まで含めた名前
    '''

    __tablename__ = 'methods'

    id = decl.Column(al.Integer, primary_key=True, autoincrement=True)
    signature = decl.Column(al.Unicode(512), nullable=False)
    name = decl.Column(al.Unicode(255), nullable=False)
    fqname = decl.Column(al.Unicode(1024), nullable=False)
    class_ = decl.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)
    return_type = decl.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)
    argcount = decl.Column(al.Integer)



class MethodArg(Base):
    u'''
    メソッドの引数

    :param int method_id: 対象メソッド (PK, FK)
    :param int order: メソッドの番号 (PK)
    :param int type: 型名 (FK)
    '''

    __tablename__ = 'methodargs'

    method_id = decl.Column(al.Integer, al.ForeignKey('methods.id'), primary_key=True)
    order = decl.Column(al.Integer, primary_key=True)
    type = decl.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)





