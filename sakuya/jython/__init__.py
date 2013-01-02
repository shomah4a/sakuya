#-*- coding:utf-8 -*-

import os
import subprocess

import simplejson
import sakuya



def get_path(mod):

    return os.path.dirname(os.path.dirname(mod.__file__))



def run_jython(args, line_handler):
    u'''
    jython で動かす
    '''

    env = os.environ.copy()

    spath = get_path(sakuya)

    entry = os.path.join(os.path.dirname(sakuya.__file__), 'jython', 'command.py')

    env['JYTHONPATH'] = ':'.join([get_path(simplejson), spath])

    p = subprocess.Popen(['jython', entry]+list(args), env=env, stdout=subprocess.PIPE)

    for line in p.stdout:
        line_handler(line)

    retcode = p.wait()

    if retcode != 0:
        pass




if __name__ == '__main__':
    import sys
    run_jython(sys.argv[1:])

