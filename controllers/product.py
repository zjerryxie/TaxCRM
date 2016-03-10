from plugin_dialog import grid2
from gluon.storage import List

def validate(form):
    # validate categories as comma delimited string
    cats = form.vars.categories.split(",")
    for cat in cats:
        catrec = db(db.category.category2==cat).select().first()
        if not catrec:
            form.errors.categories = "%s is not a valid category"%cat
            return

def edit():
    """ product master ==> web product, product_description, product_category """
    id=request.args(0)
    form = SQLFORM(db.product, id, _class="well", _id="productform")

    if form.process(onvalidation=validate).accepted:
        # propogate changes to the web database
        wp=web.oc6t_product
        wd=web.oc6t_product_description
        
        # update product matching fields in each file. 
        if id:
            webid=web(wp.model==id).select().first().product_id
            # link web.oc6t_product.model=>db.product.id
            web(wp.model==id).update(**wp._filter_fields(form.vars))
            web((wd.product_id==webid) & (wd.language_id==1)).update(**wd._filter_fields(form.vars))
        # add new product
        else:
            webid=wp.insert(model=id, **wp._filter_fields(form.vars))
            wd.insert(product_id=webid, language_id=1, **wd._filter_fields(form.vars))

        # propagate productcategory
        wpc=web.oc6t_product_to_category
        wcd=web.oc6t_category_description
        web(wpc.product_id==webid).delete()
        for cat in form.vars.categories.split(","):
           webcat = web((wcd.name==cat ) & (wcd.language_id==1)).select().first()
           wpc.insert(product_id=webid, category_id=webcat.category_id)
        DAL.distributed_transaction_commit(db, web)

    sectionlist = (('id', 'Product'),
              ('created_on', ''))
    form = form.ctform(sectionlist=sectionlist)
    response.view='default/edit.'+request.extension
    return dict(form=form, componentheader=H1("product"))

def grid():
    fieldnames = ['id', 'modified_on', 'name', 'price']
    
    action, table, id=request.args(0), request.args(1), request.args(2)
    if action in ["new", "edit"]:
        request.args=List(id)
        return product()

    grid = SQLFORM.grid(db.product, 
                    deletable=False,
                    maxtextlength=100,
                    orderby='modified_on desc',
                    fields=[db.product[fieldname] for fieldname in fieldnames],
                    **grid2.defaults1())

    response.view='default/grid.'+request.extension
    return dict(grid=grid, componentheader=H1("Product"))

def product():
    id=request.args(0)
    # if not yet created then add record to provide primary key for the related grids
    if not id:
        id = db.customer.insert()
    response.view='default/product.html'
    return dict(id=id)   