from plugin_dialog import grid2

def edit():
    db.event.customer.default=request.vars.customer
    
    form = SQLFORM(db.event, request.args[0])
    if form.process().accepted:
        response.js = "closedialog();refresh('event');"
    else:
        response.js="$('#myModalLabel').text('Event');opendialog();"

    form = form.ctform()
    response.view='default/edit.load'
    return dict(form=form)

def grid():
    action, table, id=request.args(0), request.args(1), request.args(2)
    if action in ["new", "edit"]:
        request.args=[id]
        return edit()

    query=db.event.id>0
    fieldnames = ['id', 'customer', 'date_', 'time_', 'subject', 'completed', 'modified_by']
    gridargs = grid2.defaults1()
    gridargs.update(
        create=False,
        details=False,
        deletable=True,
        maxtextlength=100,
        orderby = 'date_ desc, time_ desc',
        fields=[db.event[fieldname] for fieldname in fieldnames])

    if request.vars.customer:
        query = (db.event.customer == request.vars.customer)
        gridargs.update(
            fields=[db.event[fieldname] for fieldname in fieldnames if fieldname != "customer"],
            create=True)

    grid = SQLFORM.grid(query, **gridargs)
    grid2.dialogButtons(grid, ["new", "edit"])

    response.view='default/grid.'+request.extension
    return dict(grid=grid, componentheader=H1("Event"))