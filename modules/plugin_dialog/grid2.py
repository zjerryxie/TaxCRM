""" additional functions for a SQLFORM.grid """

import uuid
from gluon import *
request=current.request
T=current.T

def search_form(self,url): 
    """ smaller, simpler search form for multiple grids on a page """
    form = FORM('', 
        INPUT(_name='keywords',_value=request.vars.keywords, 
               _style='width:200px;', 
               _id='keywords'), 
         INPUT(_type='submit',_value=T('Search')), 
         INPUT(_type='submit',_value=T('Clear'), 
         _onclick="jQuery('#keywords').val('');"), 
         _method="GET",_action=url) 
    return form 

def defaults1():
    """ common defaults for multiple grids on a page """
    return dict(
        # unique formname otherwise paginate and back buttons redirect to wrong grid
        # note need to remove special chars in uuid as formname used as method name in grid search
        formname=str(uuid.uuid4()).replace("-",""),

        # reduce space
        searchable=True,
        search_widget=search_form,
        csv=False,
        paginate=5)

def dialogButtons(grid, actions):
    """ change button actions (e.g. ["new", "edit"]) to open dialog rather than inline form """

    for elem in _getButtons(grid):
        if elem['_href']:
            for action in actions:
                if _isAction(elem['_href'], action):
                    elem['_onclick']="getdialog('%s')"%elem['_href']
                    del elem['_href']
                    del elem['cid']
                    break

def pageButtons(grid, actions):
    """ change button actions to open new page rather than inline form """
    for elem in _getButtons(grid):
        if elem['_href']:
            for action in actions:
                if _isAction(elem['_href'], action):
                    del elem['cid']
                    break

def _getButtons(grid):
    """ return list of all buttons """

    # get topbuttons
    try:
        topbuttons=grid.element('.web2py_console').elements('.button')
    except:
        topbuttons=[]
    
    # get rowbuttons
    rowbuttons=[]
    rows=grid.elements('.row_buttons')
    for row in rows:
        buttons=row.elements('.button')
        rowbuttons.extend(buttons)

    return topbuttons+rowbuttons

def _isAction(url, action):
    """ detects if url contains the action (e.g. new/edit/delete/view) """
    return "/%s/"%action in url or "/%s?"%action in url or url.endswith("/%s"%action)