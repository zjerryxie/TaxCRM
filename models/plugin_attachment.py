# contains file attachments for all tables. Linked to table/row via parentname/parentid
db.define_table('plugin_attachment_attachment',
		Field('parentname'),
		Field('parentid', 'integer'),
		Field('sortorder', 'integer'),
		Field('file1', 'upload', readable=False, writable=False),
		Field('filename', writable=False, 
			represent=lambda value, row: A(row.filename, _href=URL(c='default', f='download', args=row.file1))))