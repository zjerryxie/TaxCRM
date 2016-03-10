from plugin_dialog import grid2
from gluon.storage import List
from calc import calc_salesorder, calc_orderline

def edit():
    
    db.orderline.salesorder.default=request.vars.salesorder
    orderline=db.orderline[request.args[0]]
    
    form = SQLFORM(db.orderline, orderline)
    if form.process().accepted:
        salesorder=db.salesorder[orderline.salesorder]
        calc_orderline(db, db.orderline[orderline])
        calc_salesorder(db, salesorder)
        response.js="closedialog();refresh('orderline');"
    else:
        response.js="$('#myModalLabel').text('Orderline');opendialog();"
        response.flash=""

    response.js+="$('.btn-primary').css('display', 'inline');"

    form = form.ctform()
    response.view='default/edit.load'
    return dict(form=form)

def grid():
    action, table, id=request.args(0), request.args(1), request.args(2)
    if action in ["edit"]:
        request.args=List([id])
        return edit()
    if action in ["new"]:
        request.args=List()
        return select()
    if action in ["delete"]:
        request.args=[id]
        return delete()

    fieldnames = ['id', 'salesorder', 'product', 'price', 'quantity', "total"]
    query = (db.orderline.id > 0)
    gridargs=dict(
        fields=[db.orderline[fieldname] for fieldname in fieldnames],
        **grid2.defaults1())

    if request.vars.salesorder:
        gridargs.update(
            fields=[db.orderline[fieldname] for fieldname in fieldnames if fieldname != "salesorder"])
        query = (db.orderline.salesorder == request.vars.salesorder)
    
    gridargs.update(searchable=False)
    grid = SQLFORM.grid(query, **gridargs)
    grid2.dialogButtons(grid, ["new", "edit"])

    if request.vars.salesorder:
        log.info(request.vars.salesorder)
        total = str(db.salesorder[request.vars.salesorder].price)
        grid.element('tbody', replace=lambda t: t + TFOOT(TR(TD(), TD("Order "+request.vars.salesorder), \
                                                 TD(_colspan=2), TD(total), TD(), _class="total")))

    response.view='default/grid.'+request.extension
    return dict(grid=grid, componentheader=H1("Orderline"))

################# ajax functions ########################################
def select():
    """ popup grid from which to select a product to add """
    # add button
    links=[lambda row: A(SPAN(_class="icon plus icon-plus glyphicon glyphicon-plus"),
                    SPAN("Add", _class="buttontext button", _title="Add record to database"),
                    _class="button btn btn-default", 
                    _onclick="$.web2py.ajax('%s')"%URL('add',args=[row.id], vars=dict(salesorder=request.vars.salesorder)))]

    fieldnames = ['id', 'modified_on', 'name', 'price']

    request.function="select"

    query = db.product.id>0
    gridargs = grid2.defaults1()
    gridargs.update(
            create=False, 
            details=False,
            editable=False,
            deletable=False,
            csv=False,
            maxtextlength=25,
            paginate=10, 
            fields=[db.product[fieldname] for fieldname in fieldnames],
            orderby='modified_on desc',
            links=links)

    grid = SQLFORM.grid(query, **gridargs)

    response.js="$('#myModalLabel').text('Select product');opendialog();"
    # show search buttons and hide save button
    response.js+="$('#modal-body form :submit').css('display', 'inline');"
    response.js+="$('.btn-primary').css('display', 'none');"
    response.view = 'default/grid.load'
    return dict(grid=grid) 

def add():
    """ adds an orderline to the salesorder """
    product=db.product[request.args[0]]
    orderline = db.orderline.insert(salesorder=request.vars.salesorder,
                                    product = product.id,
                                    price = product.price)
    calc_orderline(db, db.orderline[orderline])
    calc_salesorder(db, db.salesorder[request.vars.salesorder])
    response.js = "closedialog();refresh('orderline')"
    return dict()

def delete():
    """ deletes orderline from salesorder and refreshes the related components """ 
    orderline = db.orderline[request.args[0]] 
    db(db.orderline.id==orderline.id).delete()
    calc_salesorder(db, db.salesorder[orderline.salesorder])
    log.info("END OF DELETE" + str(orderline.salesorder) + str(db.salesorder[orderline.salesorder].price))
    response.js = "refresh('orderline')"
    return dict()