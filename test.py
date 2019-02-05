import CreateTable as db



'''
with db.session_scope() as session:
	task_row = URLTask( url_id=1, 
						url='www.google.com', 
						timestamp=0,
						duration=1,
						status=2,
						priority=1 )

	text_row = URLText( text_id=1, 
						url_id=1,
						timestamp=20190204,
						text='Try to see if ForeignKey works')
	session.add(task_row)
	session.add(text_row)
	session.commit()

'''



with session_scope() as session:
	row = session.query(URLTask).filter( URLTask.url_id == 1 ).first()
	print('Retrieving: ', row.url_id, row.url)

	