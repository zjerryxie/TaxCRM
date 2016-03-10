from plugin_dialog import grid2
from gluon.storage import List
import os

def grid():
    action, table, id=request.args(0), request.args(1), request.args(2)
    if action in ["edit"]:
        request.args=List([id])
        return salesorder()
    if action in ["new"]:
        request.args=List()
        return salesorder()

    query = (db.salesorder.id > 0)
    fieldnames = ['id', 'customer', 'price']
    gridargs = grid2.defaults1()
    gridargs.update(
                deletable=False,
                maxtextlength=100,
                orderby='modified_on desc',
                fields=[db.salesorder[fieldname] for fieldname in fieldnames])

    if request.vars.customer:
        gridargs.update(fields=[db.salesorder[fieldname] for fieldname in fieldnames if fieldname !="customer"])
        query = (db.salesorder.customer == request.vars.customer)
    
    grid = SQLFORM.grid(query, **gridargs)
    grid2.pageButtons(grid, ["new", "edit"])
    
    response.view='default/grid.'+request.extension
    return dict(grid=grid, componentheader=H1("Order"))

def salesorder():
    id=request.args(0)
    # if not yet created then add record to provide primary key for the related grids
    if not id:
        id = db.salesorder.insert(customer=request.vars.customer)

    response.view='default/salesorder.html'
    return dict(id=id)