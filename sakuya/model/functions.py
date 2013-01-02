#-*- coding: utf-8 -*-

import json


from sqlalchemy.sql import functions
from sqlalchemy import sql

from sakuya import constants
from . import tables, session



def create_type(sess, fqname):
    u'''
    クラスなり型なりを追加
    '''

    t = tables.Type.__table__

    query = sql.select([t.c.id], t.c.fqname == fqname, t)

    result = sess.execute(query).fetchall()

    if result:
        return result[0][0]

    name = fqname.split('.')[-1]

    typ = tables.Type(name=name, fqname=fqname)

    with sess.begin():
        sess.add(typ)

    query = sql.select([t.c.id], t.c.fqname == fqname, t)

    result = sess.execute(query).fetchone()[0]

    return result



def make_signature(fqname, parameters, rtype):
    u'''
    シグネチャを作る
    '''

    return '{0} {1}({2})'.format(rtype, fqname, ', '.join(map(str, parameters)))



def create_method(sess, name, fqname, cls, rtype, parameters):
    u'''
    メソッドと引数情報を登録
    '''

    method = tables.Method.__table__

    cls_id = create_type(sess, cls)
    rtype_id = create_type(sess, rtype)
    parameter_ids = map(lambda x: create_type(sess, x), parameters)
    signature = make_signature('.'.join([str(cls_id), name]), parameter_ids, rtype_id)


    with sess.begin():
        meth = tables.Method(name=name,
                             fqname=fqname,
                             signature=signature,
                             class_=cls_id,
                             return_type=rtype_id,
                             argcount=len(parameters))

        sess.add(meth)

    query = sql.select([method.c.id],
                       sql.and_(method.c.name == name,
                                method.c.fqname == fqname,
                                method.c.class_ == cls_id,
                                method.c.return_type == rtype_id,
                                method.c.signature == signature),
                       method).order_by(method.c.id.asc())

    result = sess.execute(query).fetchall()

    mid = result[-1][0]

    with sess.begin():

        for order, pid in enumerate(parameter_ids):

            arg = tables.MethodArg(method_id=mid,
                                   order=order,
                                   type=pid)
            sess.add(arg)



def create_from_json(jsonstr):
    u'''
    JSON から登録
    '''

    data = json.loads(jsonstr)

    typ = data.get('type')

    if typ != constants.JAVA_METHOD:
        return

    fqname = data.get('fully_qualified')
    name = data.get('name')
    cls = data.get('class')
    parameters = data.get('parameters')
    rtype = data.get('rtype')

    with session.Session() as sess:
        create_method(sess, name, fqname, cls, rtype, parameters)




def _search_with_args(sess, ret_type, parameters):
    u'''
    返り値型と引数の型による検索
    '''

    u'''
    -- 大体こんなことがしたい
    SELECT method.id, method.name, method.fqname FROM methods
      JOIN types rtype on methods.return_type = rtype.id
      JOIN methodargs marg on methods.id = marg.method_id
      JOIN types atype on marg.type = atype.id
    WHERE
      method.argcount = ${len(parameters)} AND
      rtype.name = ${rtype} AND
      methodargs.order = ${paramidx} AND
      atype.name = ${parameters[paramidx]}
      ...
    GROUP BY method.id
    HAVING
      COUNT(*) = ${len(parameters)}
    '''

    method = tables.Method.__table__
    marg = tables.MethodArg.__table__
    rtype = tables.Type.__table__.alias('rtype')
    atype = tables.Type.__table__.alias('atype')

    joined = method.join(marg, method.c.id == marg.c.method_id)
    joined = joined.join(atype, marg.c.type == atype.c.id)
    joined = joined.join(rtype, method.c.return_type == rtype.c.id)

    def make_param_query(idx, param):

        return sql.and_(marg.c.order == idx,
                        atype.c.name == param)

    where = sql.and_(method.c.argcount == len(parameters),
                     rtype.c.name == ret_type,
                     *[make_param_query(idx, param)
                       for idx, param in enumerate(parameters)])

    sel = sql.select([method.c.id, method.c.name, method.c.fqname],
                     where, joined).group_by(method.c.id).having(functions.count() == len(parameters))

    results = sess.execute(sel).fetchall()

    for x in results:
        print x[2]



def _search_without_args(sess, ret_type):
    u'''
    引数の型だけで検索
    '''

    u'''
    -- 大体こんなことがしたい
    SELECT method.id, method.name, method.fqname FROM methods
      JOIN types rtype on methods.return_type = rtype.id
    WHERE
      method.argcount = 0 AND
      rtype.name = ${rtype} AND
    '''

    method = tables.Method.__table__
    rtype = tables.Type.__table__.alias('rtype')

    joined = method.join(rtype, method.c.return_type == rtype.c.id)

    where = sql.and_(method.c.argcount == 0,
                     rtype.c.name == ret_type)

    sel = sql.select([method.c.id, method.c.name, method.c.fqname],
                     where, joined)

    results = sess.execute(sel).fetchall()

    for x in results:
        print x[2]




def search_by_type(sess, ret_type, parameters):
    u'''
    型で検索
    '''

    if parameters:
        return _search_with_args(sess, ret_type, parameters)
    return _search_without_args(sess, ret_type)


