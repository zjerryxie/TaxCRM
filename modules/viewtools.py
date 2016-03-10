# -*- coding: utf-8 -*-
from gluon.storage import Storage
from gluon import *
from gluon import current
import logging as log
request=current.request
T=current.T

def load2(**args):
    """ LOAD with url to enable component refresh
    
    page with multiple components loads much faster with ajax=False
    need to store url with component to enable refresh
    data-w2p_remote is set to url but only when ajax=True
    data-w2_remote cannot be set manually as contains hyphen
    ==> solution is to use load2 with c, f; and set _url parameter

    (Note also do not allow url parameter as when set LOAD sets ajax=True even with explicit ajax=False)
"""
    s=Storage(**args)
    url=URL(c=s.c, f=s.f, args=s.args, vars=s.vars, extension=s.extension)
    # note grids have to be ajax_trap for pagination to work
    return LOAD(_url=url, ajax_trap=True, **args)