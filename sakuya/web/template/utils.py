#-*- codijg: utf-8 -*-


def get_package(fqname):

    return '.'.join(fqname.split('.')[:-1])



def get_classname(fqname):

    return fqname.split('.')[-1]
