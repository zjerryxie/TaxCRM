import logging as log

def calc_orderline(db, orderline):
	log.info(type(orderline))
	log.info(orderline.id)
	log.info(orderline.price)
	log.info(orderline.quantity)
	orderline.total =  orderline.price * orderline.quantity
	orderline.update_record()

def calc_salesorder(db, salesorder):
	total = 0
	for line in db(db.orderline.salesorder==salesorder.id).select():
		total = total + line.total
	salesorder.price = total
	salesorder.update_record()