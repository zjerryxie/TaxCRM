requirements
------------

install AMPPS
goto ampps installation and install opencart
	rename config-dist.php and admin/config-dist.php to config.php
	goto 127.0.0.1:80 [note localhost fails]
	check database name from phpmyadmin
	set password to mysql, database name as above, prefix oc_
install web2py
clone crm to web2py/applications/crm

servers
-------

apache port 80
	localhost/opencart
	localhost/opencart/admin (admin/pass)
mysql port 3306
	drives opencart database
	localhost/phpmyadmin (root/a)
web2py port 8000
	run under python 2 (not py3 compatible)
	crm system manages master database on sqlite


opencart changes
----------------

checkout/cart
	remove coupon, gift voucher, shipping, only show total
checkout/checkout
	remove company name, delivery method please select shipping rate
	payment method
	only show total

models
------

db - sets up the database connection, logging etc..
dbtables - defines the tables
menu - the menu!

databases
---------

opencart used for website. this is php/mysql based
sqlite used as master database

modules
-------

crmsetup
	deletedata
		utlity to delete all tables in crm database except auth and those in the exclude list.
		used during testing to reset database.
	populate
		populates database with test data
		extracts some data from opencart

view
	ctform
		converts ctform to columntable format
	viewtools
		utlities for views

static
------

crm.css
crafty_*
	for uk postcode lookup

views
-----

generic - edit, grid
shared - historyform, files
specific - customer, salesorder

controllers
-----------

one for each table e.g. customer, order, product....

plugin_attachment
-----------------

To allow attachments to be added to a record:
	set parentname and parentid for the record it will be attached to
	add this to the view
		{{include 'plugin_attachment/attachments.html'}}
	
plugin_dialog
-------------

changes add/edit grid buttons to replace inline with dialog boxes or open a new page