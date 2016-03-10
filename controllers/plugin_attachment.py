""" 
add/delete/display file attachments including drag/drop from desktop and other websites
"""

import os
import urllib2
from storage import Storage
from io import BytesIO
import base64, mimetypes

v=request.vars
tab=db.plugin_attachment_attachment

def edit():
    """ demo controller that returns a simple edit form with attachments """
    form=SQLFORM(db.plugin_attachment_customer, request.args(0))
    return dict(form=form, id=request.args(0))

def index():
    redirect(URL(f='edit.html/1'))

def display():
    """ display attachments with image; filename; download button; delete button; """

    attachments=db((tab.parentname==v.parentname) & (tab.parentid==v.parentid)).select(orderby='sortorder')
    confirm="if(!confirm(w2p_ajax_confirm_message||'Are you sure you want to delete this object?')) \
                     {var e = arguments[0] || window.event; e.cancelBubble=true; if (e.stopPropagation) e.stopPropagation();return false;};"
    
    rows=[]
    for attachment in attachments:
        ext = attachment.filename.split('.')[-1]
        if ext == attachment.filename:
            ext="file"
        if ext.lower() in ["png", "jpe", "jpg", "jpeg", "gif", "bmp"]:
            image=URL('default', 'download', args=attachment.file1)
        else:
            image=URL('static/plugin_attachment/fileicons', ext + '.png')
        rows.append(TR(
                IMG(_style="max-width: 100px; max-height:100px", _src=image),
                A(attachment.filename.split('/')[-1], _href=URL('default', 'download', args=attachment.file1)),
                BUTTON('Delete', _class='btn', _onclick="%s ajax('%s');jQuery(this).closest('tr').remove();" %(confirm, URL('delete', args=attachment.id)))
                ))
    grid=TABLE(rows)
    
    response.view='plugin_attachment/grid.load'
    return dict(grid=grid)

def grid():
    """ show as grid without images """
    
    grid=SQLFORM.grid(tab, create=False, editable=False, deletable=False, details=False)
    response.view='plugin_attachment/grid.'+request.extension
    return dict(grid=grid)

def add():
    """ v.files added as attachments (allows drag/drop from the desktop)
        v.url added as attachment (allows drag/drop of a file url or inline image from another webpage) """   
    # fetch url as a file object
    if v.url:
        try:
            # inline image data
            if v.url.startswith("data:"):
                image=imageparser(v.url)
                v.files=Storage(file=BytesIO(image.raw_bytes), filename="inlineimage"+image.ext)
            # URL file
            else:
                # note filenames truncated else file.store raises exception
                v.files=Storage(file=urllib2.urlopen(v.url), filename=v.url[:75])
        except:
            log.exception("failed to get url: %s"%v.url)
            raise HTTP(404)
        
    # set sortorder
    maxsort=tab.sortorder.max()
    attachments=db((tab.parentname==v.parentname) & (tab.parentid==v.parentid)).select(maxsort).first()
    try: sortorder=attachments[maxsort]+1
    except: sortorder=0

    # add to database
    if not isinstance(v.files,list): v.files=[v.files]
    for f in v.files:
        coded_filename=tab.file1.store(f.file, f.filename)
        tab.insert(parentname=v.parentname,
                 parentid=v.parentid,
                 file1=coded_filename,
                 filename=f.filename,
                 sortorder=sortorder)
        sortorder+=1

def delete():
    """ delete attachment """

    os.remove('%s/%s/%s'%(request.folder, "uploads",tab[request.args(0)].file1))
    db(tab.id==request.args(0)).delete()

class imageparser(object):
    """ parse inline images """
    
    mime_type = None
    ext = None
    raw_bytes = None

    def __init__(this, url):
        this.url=url

        metadata, encoded = v.url.rsplit(",", 1)
        _, metadata = metadata.split("data:", 1)
        parts = metadata.rsplit(";", 1)
        if parts[-1] == "base64":
            this.raw_bytes = base64.b64decode(encoded)
            parts = parts[:-1]
        else:
            this.raw_bytes=encoded
        if not parts or not parts[0]:
            parts = ["text/plain;charset=US-ASCII"]
        
        this.mime_type = parts[0]
        this.ext=mimetypes.guess_extension(this.mime_type)