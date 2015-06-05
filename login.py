# -*- coding: utf-8 -*-
#Logic Related to Signup

@app.route('/login')
def login():
	return render('KOISTUDYS2', '', 'login')

@app.route('/login/submit', methods=['POST'])
def login_submit():
	import dbhandler
	import bcrypt
	import datetime
	try:
		pw = dbhandler.col_members.find({"username": request.form['username']})[0]['password']
		if bcrypt.hashpw(request.form['password'], pw) == pw:
			session['username'] = request.form['username']
			log = {"date": datetime.datetime.now(), "type": "login", "result": "succeed", "username": request.form['username'], "ip": request.remote_addr}
			dbhandler.col_logs.insert_one(log)
			return redirect('/')
		else:
			log = {"date": datetime.datetime.now(), "type": "login", "result": "wrongpw", "username": request.form['username'], "ip": request.remote_addr}
			dbhandler.col_logs.insert_one(log)
			return render('KOISTUDYS2', '', 'login_err_pw')
	except IndexError:
		log = {"date": datetime.datetime.now(), "type": "login", "result": "wrongusername", "username": request.form['username'], "ip": request.remote_addr}
		dbhandler.col_logs.insert_one(log)
		return render('KOISTUDYS2', '', 'login_err_username')

@app.route('/logout')
def logout():
	del session['username']
	return redirect('/')