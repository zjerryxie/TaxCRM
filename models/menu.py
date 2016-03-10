""" custom menus """

response.menu=[]

if DEBUG:
   response.menu+=[(T('Clean'), False, URL(c='default', f='clean'))]
   response.menu+=[(T('Delete'), False, URL(c='default', f='delete'))]
   response.menu+=[(T('Populate'), False, URL(c='default', f='populate'))]
   response.menu+=[(T('Errors'), False, URL(a='admin', c='default', f='errors.html',
                    args=[request.application, "old"]))]

response.menu+=[(T('Customers'), False, URL(c='customer', f='grid'))]
response.menu+=[(T('Products'), False, URL(c='product', f='grid'))]
response.menu+=[(T('Orders'), False, URL(c='salesorder', f='grid'))]
response.menu+=[(T('Orderlines'), False, URL(c='orderline', f='grid'))]
response.menu+=[(T('Events'), False, URL(c='event', f='grid'))]