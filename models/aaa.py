# -*- coding: utf-8 -*-

################################ DEBUGGING ######################################################################
import os
import logging
try:
    from logconfig import log
except:
    log = logging.getLogger()

# comment to turn off debugging
log.setLevel(logging.DEBUG)

DEBUG=log.isEnabledFor(logging.DEBUG)
################################ IMPORTS ##############################################################################

if DEBUG: from gluon.custom_import import track_changes; track_changes(True)

# web2py
#from gluon.tools import *
from globals import current  
from storage import Storage

# python
import datetime
import time
import decimal

# crm modules
import ctform
from viewtools import load2

################################ WEB2PY SETUP ###################################################################

if request.controller=="default" and request.function=="delete":
    log.info("deleting everything")
    db = DAL('sqlite://storage.sqlite', migrate=False, fake_migrate=True)
else:
    db = DAL('sqlite://storage.sqlite', pool_size=10, lazy_tables = True, migrate=DEBUG)

# db contains master data. web contains data shown on the website 
webstring = "mysql://root:mysql@localhost:3306/ocar199"
testimages="C:/Program Files (x86)/Ampps/www/ocart2/image/catalog/demo"

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

response.generic_patterns = ['*'] if request.is_local else []
if not DEBUG:
    response.optimize_css = 'concat,minify,inline'
    response.optimize_js = 'concat,minify,inline'

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.define_tables(username=False, signature=True)
db.define_table('signature')
auth.signature.created_on.readable=True
auth.signature.modified_on.readable=True
auth.signature.created_by.readable=True
auth.signature.modified_by.readable=True
#### this seems to fail during populate on latest web2py
db._common_fields.append(auth.signature)

############################# CONTROLLER INIT ##########################################################################

# log request. shows vars with files as <filename> and truncates rest to 20.
vars2=dict()
for key, val in request.vars.items():
    try: vars2[key]="<"+val.filename+">"
    except: vars2[key]=str(val) if len(str(val))<20 else str(val)[:20]+"..."
log.info("%s/%s vars=%s args=%s ajax=%s" %(request.controller, request.function, str(vars2), request.args, request.ajax))

# require login for all controllers except default/user
if auth.user is None and not (request.controller=='default'):
    url = URL('default','user', args='login', vars=dict(_next=request.url))
    redirect(url) 

# add history except for ajax, create record, download
if not request.ajax and \
not (request.function in ("edit") and len(request.args)==0) and \
not request.function in ("download"):
    session.setdefault("history", [])
    url=URL(f=request.function, extension=request.extension, args=request.args)
    if len(session.history)>0 and session.history[-1]==url:
        pass
    else:
        session.history.append(URL(f=request.function, extension=request.extension, args=request.args))