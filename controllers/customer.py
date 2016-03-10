# -*- coding: utf-8 -*-

def edit():
    form = SQLFORM(db.customer, request.args(0), _class="well", _id="customerform")
    if form.process().accepted:
        pass
    
    sectionlist = (('id', 'Contact Details'),
                   ('created_on', ''))
    form = form.ctform(sectionlist=sectionlist)

    response.view='default/edit.load'
    return dict(form=form)

def grid():
    action, table, id=request.args(0), request.args(1), request.args(2)
    if action in ["new", "edit"]:
        redirect(URL(f='customer', args=[id]))

    fieldnames = ['id', 'name', 'postcode', 'home_phone', 'mobile_phone']
    grid = SQLFORM.grid(db.customer, 
                    deletable=False,
                    maxtextlength=100,
                    fields=[db.customer[fieldname] for fieldname in fieldnames])

    response.view='default/grid.html'
    return dict(grid=grid, componentheader=H1("Customer"))

def customer():
    id = request.args(0)
    # if not yet created then add record to provide primary key for the related grids
    if not id:
        id = db.customer.insert()
       
    response.view='default/customer.html'
    return dict(id=id)