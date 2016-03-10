import logging as log

def calc_orderline(db, orderline):
	line = db.orderline[orderline]
	line.total =  line.price * line.quantity
	line.update_record()

def calc_salesorder(db, salesorder):
	total = 0
	for line in db(db.orderline.salesorder==salesorder).select():
		total = total + line.total
	salesorder.price = total
	salesorder.update_record()