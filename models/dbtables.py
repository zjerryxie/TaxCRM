""" contains table definitions and calls populate """

############### shared functions #########################################################

def html(field, value): 
    """ widget for wysiwyg html editing """
    return TEXTAREA(_id = str(field).replace('.','_'), _name=field.name, 
                  _class='html', value=XML(value, sanitize=True), _cols=800, _rows=10)
    
def postcode(field, value):
    """ widget for UK postcode to address lookup using craftyclicks.co.uk  
    Set id of address fields to prefix + address1, address2, address3, town, county, postcode 
    Prefix can be blank but must be different for each address on same page e.g. bill_, ship_ """
    return CAT(
           INPUT(_name=field.name,
                 _id='%s_%s' % (field._tablename, field.name),
                 _class=field.type, value=value, _style='width:auto', requires=field.requires),
           A('Lookup address', _class='btn btn-default', _id='%s_%s_button' % (field._tablename, field.name),
                               _onclick='postcodeLookup(this); return false'),
           DIV(_id='postcode_results'))

########################### CRM TABLES START HERE ############################################

db.define_table('customer',
        Field('title', requires=IS_IN_SET(['Mr', 'Mrs', 'Ms'], zero=None)),
        Field('name', length=256, requires=[IS_NOT_EMPTY()]),
        Field('address1', length=256),
        Field('address2', length=256),
        Field('address3', length=256),
        Field('town', length=256),
        Field('county', length=256),
        Field('postcode', length=8, widget=postcode),
        Field('home_phone', length=15),
        Field('mobile_phone', length=15),
        Field('email', length=15, requires=IS_EMPTY_OR(IS_EMAIL())),
        Field('sex', requires=IS_IN_SET(('Male', 'Female'), zero=None)),
        Field('date_of_birth', 'date', requires=IS_EMPTY_OR(IS_DATE())),
        Field('age', 'integer', writable=False),
        Field('source', requires=IS_IN_SET(('Web', 'Phone', 'Direct Mail', 'Other'), zero=None)),
        Field('no_marketing', 'boolean'),
        format=lambda r: A(r.name, _href=URL(c='customer', f='customer.html', args=[r.id])))

######################## PRODUCT ########################################################################            

db.define_table('category',
        Field('category1'),
        Field('category2'),
        format=lambda r: r.category1+" "+r.category2)

db.define_table('product',
        Field('name'),
        Field('price', 'decimal(8,2)', requires=IS_DECIMAL_IN_RANGE(0.01, 30.00)), 
        Field('quantity', 'integer', default=0),
        Field('description', type='text', requires=IS_NOT_EMPTY(), notnull=True, widget=html),
        Field('categories'),
        format=lambda r: A(r.name, _href=URL(c='product', f='edit.html', args=[r.id])))

########################## EVENTS ##################################################################

db.define_table('event',
        Field('customer', 'reference customer', writable=False),
        Field('subject', length=150),
        Field('date_', 'date', default=request.now.date, notnull=True),
        Field('time_', 'time', default=request.now.time),
        Field('completed', 'boolean'))

######################### SALES #####################################################################

db.define_table('salesorder',
        Field('customer', 'reference customer', writable=False),
        Field('price', 'decimal(8,2)', writable=False))

db.define_table('orderline',
        Field('salesorder', 'reference salesorder', writable=False),
        Field('product', 'reference product', writable=False),
        Field('price', 'decimal(8,2)', writable=False),
        Field('quantity', 'integer', requires=IS_INT_IN_RANGE(1,11), default=1),
        Field('total', compute=lambda row: row.price*row.quantity))


######################## OPENCART CATEGORY AND PRODUCT ########################################################################

def define_web():
    """ db holds crm data and is master data for product
    web holds opencart data visible on web """
 
    web = DAL(webstring, pool_size=10, lazy_tables = True, migrate=False)

    # category
    web.define_table('oc6t_category',
        Field('category_id', type='id', notnull=True, writable=False),
        Field('parent_id', type='integer', default='0', notnull=True, writable=False),
        Field('top', type='integer', notnull=True, writable=False))
    
    web.define_table('oc6t_category_description',
        Field('category_id', type='integer', notnull=True, writable=False),
        Field('language_id', type='integer', notnull=True, writable=False),
        Field('name', type='text', length=255, notnull=True),
        Field('description', type='text', length=65535, notnull=True),
        primarykey=['category_id', 'language_id'],
        format=lambda r: r["description"])

    # product
    web.define_table('oc6t_product',
        Field('product_id', type='id', notnull=True),
        Field('model', type='text', notnull=True),
        Field('quantity', type='integer', default='0', notnull=True),
        Field('image', type='text', length=255),
        Field('price', type='decimal(15,4)'))
    
    web.define_table('oc6t_product_description',
        Field('product_id', type=web.oc6t_product, notnull=True),
        Field('language_id', type='integer', notnull=True, default=1),
        Field('name', type='text', length=25, notnull=True),
        Field('description', type='text', notnull=True, widget=html),
        primarykey=['product_id', 'language_id'])
    
    web.define_table('oc6t_product_image',
        Field('product_image_id', type='id', notnull=True),
        Field('product_id', type='integer', notnull=True),
        Field('image', type='upload', length=255),
        Field('sort_order', type='integer', default='0', notnull=True))

    # product-category
    web.define_table('oc6t_product_to_category',
        Field('category_id'),
        Field('product_id'),
        primarykey=['category_id', 'product_id'])
    
    return web

# only create link to web database if needed
web = None
if request.controller in ("product", "product_image") \
    or (request.controller=="default" and request.function in ("populate")):
    web=define_web()

# keep archive of all changes in db (not required for opencart tables)
#auth.enable_record_versioning(tables=db)