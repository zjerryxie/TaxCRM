""" controllers for the crm application that are not table specific """
exclude=[]
import os
import glob
import datetime
import logging as log
import datasetup

import boto3

def extract_w2_data(s3_path: str) -> dict:
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'S3Object': {'Bucket': 'your-bucket', 'Name': s3_path}},
        FeatureTypes=['FORMS']
    )
    return parse_textract_response(response)  # Custom parser for W-2 fields
    
def back():
    """ back to last page """
    if not session.history or len(session.history)< 2: return
    session.history.pop()
    redirect(session.history.pop())

def clean():
    os.system('cls')
    redirect(URL(a='admin', c='default', f='cleanup', args=[request.application]))

def delete():
    """ delete all data tables """
    datasetup.delete(db, request.folder)
    redirect("index")

def populate():
    """ populate db for testing """
    datasetup.populate(db, web, testimages)
    redirect("index")

def index():
    redirect(URL(c='customer', f='grid'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
