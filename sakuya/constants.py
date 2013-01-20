#-*- coding:utf-8 -*-


JAVA_PACKAGE = 'package'
JAVA_CLASS = 'class'
JAVA_METHOD = 'method'
JAVA_VARIABLET = 'VARIABLE'

MODIFIERS = [
    (0b000000000001, 'public'),
    (0b000000000010, 'private'),
    (0b000000000100, 'protected'),
    (0b000000001000, 'static'),
    (0b000000010000, 'final'),
    (0b000000100000, 'synchronized'),
    (0b000001000000, 'volatile'),
    (0b000010000000, 'transient'),
    (0b000100000000, 'native'),
    (0b001000000000, 'interface'),
    (0b010000000000, 'abstrace'),
    (0b100000000000, 'strict')
    ]

